from datetime import datetime
from typing import Any, Iterable, Optional, TypedDict

import bleach
from bleach_allowlist import markdown_tags
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from markdown import markdown

from . import notify
from .forms import generate_chousei_form_class
from .models import Event, EventDate, EventPerson, Schedule


def _get_event_info(key: str) -> tuple[Event, Iterable[EventDate]]:
    """イベント基本情報を返します

    :return: (イベント情報, イベント候補日)
    """
    event = get_object_or_404(Event, key=key)
    event_dates = event.eventdate_set.all().order_by(
        "start_datetime",
    )
    return event, event_dates


class EventDateAnswer(TypedDict):
    """イベント日付ごとの回答リスト"""

    start_datetime: datetime
    answer_list: list[Optional[dict[str, Any]]]


def _get_event_date_answer_list(
    event_dates: Iterable[EventDate],
    event_people: Iterable[EventPerson],
    schedules: Iterable[Schedule],
) -> list[EventDateAnswer]:
    """イベント日付と回答リストを返す

    :return:
        event_datesと同じ順番で EventDateAnswer のリストを返す。
        また、EventDateAnswer.answer_list の順番は event_people と同じ順番とする。
    """
    # (イベント参加者, 候補日) -> 辞書を作成
    answer_dict = {
        (schedule.event_person.pk, schedule.event_date.pk): {
            "value": schedule.answer,
            "display": schedule.get_answer_display(),
        }
        for schedule in schedules
    }
    event_date_answer_list: list[EventDateAnswer] = []
    for event_date in event_dates:
        # event_people と同じ順番で回答リストを作成
        answer_list = [
            answer_dict.get((event_person.pk, event_date.pk))
            for event_person in event_people
        ]
        event_date_answer = EventDateAnswer(
            start_datetime=event_date.start_datetime,
            answer_list=answer_list,
        )
        event_date_answer_list.append(event_date_answer)

    return event_date_answer_list


def _to_memo_html_safe(memo: str) -> str:
    """プロフィールのコンテンツをHTMLに変換します。

    この関数のレスポンスは危険なタグをサニタイズ済みのHTMLであり、
    エスケープせずに出力しても安全です。
    """

    content_html = markdown(memo, extensions=["nl2br"])
    # unsafe でレンダリングするのでHTMLをサニタイズする
    content_html_safe = bleach.clean(content_html, markdown_tags)
    return content_html_safe


def view(request: HttpRequest, key: str):
    """イベント表示画面"""
    event, event_dates = _get_event_info(key)
    event_people = event.eventperson_set.all()
    schedules = Schedule.objects.filter(event_person__event=event)
    event_date_answer_list = _get_event_date_answer_list(
        event_dates, event_people, schedules
    )
    memo = _to_memo_html_safe(event.memo)
    return render(
        request,
        "chousei/view.html",
        {
            "event": event,
            "event_date_answer_list": event_date_answer_list,
            "event_people": event_people,
            "memo": memo,
        },
    )


def add(request: HttpRequest, key: str):
    """イベント回答追加画面"""
    event, event_dates = _get_event_info(key)
    ChouseiForm = generate_chousei_form_class(event_dates)
    if request.method == "POST":
        form = ChouseiForm(data=request.POST)
        if form.is_valid():
            form.instance.event = event
            form.save_chousei_schedules()
            notify.event_schedule_added(
                to={"slack_user": event.slack_notification_user},
                event_name=event.event_name,
                event_url=reverse("chousei:view", kwargs={"key": event.key}),
                name=form.cleaned_data["name"],
            )
            return redirect("chousei:view", key)
    else:
        form = ChouseiForm()
    return render(
        request,
        "chousei/edit.html",
        {
            "event": event,
            "form": form,
        },
    )


def edit(request: HttpRequest, key: str, person_id: int):
    """イベント回答編集画面"""
    event, event_dates = _get_event_info(key)
    person = get_object_or_404(EventPerson, event=event, pk=person_id)
    ChouseiForm = generate_chousei_form_class(event_dates)
    if request.method == "POST":
        form = ChouseiForm(instance=person, data=request.POST)
        if form.is_valid():
            form.save_chousei_schedules()
            notify.event_schedule_updated(
                to={"slack_user": event.slack_notification_user},
                event_name=event.event_name,
                event_url=reverse("chousei:view", kwargs={"key": event.key}),
                name=form.cleaned_data["name"],
            )
            return redirect("chousei:view", key)

    else:
        form = ChouseiForm(instance=person)
        form.retrieve_instance_schedules()

    return render(
        request,
        "chousei/edit.html",
        {
            "event": event,
            "person": person,
            "form": form,
        },
    )
