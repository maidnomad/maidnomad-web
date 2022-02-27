from typing import Iterable

from django import forms
from django.db import transaction
from django.utils import timezone

from .choises import SCHEDULE_ANSWER_CHOISE
from .models import EventDate, EventPerson, Schedule


def _event_date_fieldname(event_date: EventDate):
    return f"eventdate_{event_date.pk}"


class ChouseiFormBase(forms.ModelForm):
    """イベント参加者情報と候補日の回答を入力するフォームの抽象基底クラス"""

    def schedule_answer_fields(self) -> list[forms.BoundField]:  # pragma: nocover
        """スケジュール回答フィールドのリストを返します"""
        raise NotImplementedError

    def save_chousei_schedules(self) -> None:  # pragma: nocover
        """フィールドの設定に基づいて EventPerson に紐づく Schedule レコードを保存します"""
        raise NotImplementedError

    def retrieve_instance_schedules(self) -> None:
        """instance に設定された EventPerson に紐づく Schedule を全て取得しフィールドの初期値を設定します"""
        schedules = self.instance.schedule_set.all()
        for schedule in schedules:
            field = self.fields.get(_event_date_fieldname(schedule.event_date))
            field.initial = schedule.answer

    class Meta:
        model = EventPerson
        fields = ["name", "comment"]

        error_messages = {
            "name": {
                "required": "名前を入力してください",
            },
        }


def generate_chousei_form_class(
    event_dates: Iterable[EventDate],
) -> type[ChouseiFormBase]:
    """イベント参加者情報と指定した候補日リストの回答を入力できるフォームクラスを生成します"""

    # 動的に追加するフィールド名とラベル、日付
    new_fieldnames = [_event_date_fieldname(event_date) for event_date in event_dates]
    # 動的にスケジュール回答選択フィールドを追加
    new_fields = {}
    for event_date, field_name in zip(event_dates, new_fieldnames):
        new_fields[field_name] = forms.ChoiceField(
            choices=SCHEDULE_ANSWER_CHOISE,
            widget=forms.widgets.RadioSelect,
            label=timezone.localtime(event_date.start_datetime).strftime(
                "%Y/%m/%d %H:%M"
            ),
            error_messages={
                "required": "回答を選んでください",
            },
        )
        new_fields[field_name].start_datetime = event_date.start_datetime

    # 抽象メソッドを oveeride する関数
    def schedule_answer_fields(self):
        return [self[field_name] for field_name in new_fieldnames]

    @transaction.atomic
    def save_chousei_schedules(self):
        self.save()
        for field_name in new_fieldnames:
            eventdate_id = int(field_name.split("_")[1])
            answer_value = self.cleaned_data[field_name]
            Schedule.objects.update_or_create(
                {
                    "answer": answer_value,
                },
                event_person=self.instance,
                event_date_id=eventdate_id,
            )

    ChouseiForm = type("ChouseiForm", (ChouseiFormBase,), new_fields)
    setattr(ChouseiForm, "schedule_answer_fields", schedule_answer_fields)
    setattr(ChouseiForm, "save_chousei_schedules", save_chousei_schedules)
    return ChouseiForm
