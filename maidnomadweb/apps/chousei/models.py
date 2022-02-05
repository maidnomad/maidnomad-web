import imp

from django.db.models import CASCADE, ForeignKey, Model
from django.db.models.fields import (
    CharField,
    DateTimeField,
    IntegerField,
    TextField,
)
from django.utils import timezone
from .choises import SCHEDULE_CHOISE


class Event(Model):
    key = CharField("キー", max_length=128, unique=True)
    event_name = CharField("イベント名", max_length=100)
    memo = TextField("メモ", blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name


class EventDate(Model):
    event = ForeignKey(Event, on_delete=CASCADE)
    start_datetime = DateTimeField("開始日時")

    class Meta:
        unique_together = ("event", "start_datetime")

    def __str__(self):
        return timezone.localtime(self.start_datetime).strftime("%Y/%m/%d %H:%m")


class EventPerson(Model):
    event = ForeignKey(Event, on_delete=CASCADE)
    name = CharField("名前", max_length=40)
    comment = TextField("コメント")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Schedule(Model):
    event_person = ForeignKey(EventPerson, on_delete=CASCADE)
    event_date = ForeignKey(EventDate, on_delete=CASCADE)
    answer = IntegerField(
        "回答",
        choices=SCHEDULE_CHOISE,
    )

    class Meta:
        unique_together = ("event_person", "event_date")
