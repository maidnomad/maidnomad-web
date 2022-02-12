from django.db.models import CASCADE, ForeignKey, Model
from django.db.models.fields import (
    CharField,
    DateTimeField,
    IntegerField,
    TextField,
)
from django.utils import timezone

from .choises import SCHEDULE_ANSWER_CHOISE


class Event(Model):
    key = CharField("キー", max_length=128, unique=True)
    event_name = CharField("イベント名", max_length=100)
    memo = TextField("メモ", blank=True)
    code_style = """
font-family: monospace;
background-color: rgb(240, 240, 240);
font-weight: bold;
padding: 0 0.5em;
"""
    slack_notification_user = CharField(
        "Slack 通知先ユーザー名",
        help_text=f"""
ユーザー名、メンバーID、チャンネル名をカンマ区切りで複数指定できます。<br />
ユーザー名は<code style='{code_style}'>@</code>,
チャンネル名は<code style='{code_style}'>#</code>をつけてください。<br />
ユーザー名は表示名・フルネームとは異なるので注意してください。""",
        max_length=255,
        blank=True,
        default=""
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name

    class Meta:
        verbose_name = "イベント"
        verbose_name_plural = "イベント"
        ordering = ["pk"]


class EventDate(Model):
    event = ForeignKey(Event, on_delete=CASCADE)
    start_datetime = DateTimeField("開始日時")

    def __str__(self):
        return timezone.localtime(self.start_datetime).strftime("%Y/%m/%d(%a) %H:%M")

    class Meta:
        verbose_name = "イベント候補日"
        verbose_name_plural = "イベント候補日"
        unique_together = ("event", "start_datetime")
        ordering = ["pk"]


class EventPerson(Model):
    event = ForeignKey(Event, on_delete=CASCADE)
    name = CharField("名前", max_length=40)
    comment = TextField("コメント", blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "イベント参加者"
        verbose_name_plural = "イベント参加者"
        ordering = ["pk"]


class Schedule(Model):
    event_person = ForeignKey(EventPerson, on_delete=CASCADE)
    event_date = ForeignKey(EventDate, on_delete=CASCADE)
    answer = IntegerField(
        "回答",
        choices=SCHEDULE_ANSWER_CHOISE,
    )

    class Meta:
        verbose_name = "スケジュール回答"
        verbose_name_plural = "スケジュール回答"
        unique_together = ("event_person", "event_date")
        ordering = ["pk"]
