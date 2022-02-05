from datetime import datetime
from hashlib import sha256
from uuid import uuid4

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Event, EventDate


class EventAdminForm(forms.ModelForm):
    default_time = forms.CharField(label="デフォルト時刻", required=False)
    dates = forms.CharField(label="候補日時", widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # 更新の時、dates フィールドに eventdate を展開する
            initial_dates = "\n".join(
                sorted(
                    [
                        timezone.localtime(eventdate.start_datetime).strftime(
                            "%Y/%m/%d %H:%M"
                        )
                        for eventdate in self.instance.eventdate_set.all()
                    ]
                )
            )
            self.fields["dates"].initial = initial_dates

    def clean_default_time(self):
        str_time = self.cleaned_data["default_time"]
        if not str_time:
            return None
        try:
            return datetime.strptime(str_time, "%H:%M").time()
        except ValueError:
            raise ValidationError("時刻のフォーマットは HH:MM 形式で入力してください")

    def clean_dates(self):
        dates_str = self.cleaned_data["dates"]
        cleaned_dates_set = set()

        for date_row in dates_str.split("\n"):
            date_row = date_row.strip()
            date_value = None
            if not date_row:
                continue
            try:
                date_value = timezone.make_aware(self._parse_datetime(date_row))
                cleaned_dates_set.add(date_value)
            except ValueError:
                raise ValidationError(f"日付のフォーマットが不正です {date_row}")
        return cleaned_dates_set

    def _parse_datetime(self, value):
        try:
            return datetime.strptime(value, "%Y/%m/%d %H:%M")
        except:
            pass
        cleaned_time = self.cleaned_data.get("default_time")
        if cleaned_time:
            try:
                value_date = datetime.strptime(value, "%Y/%m/%d")
                value_date = datetime.combine(value_date, cleaned_time)
                return value_date
            except:
                pass
        raise ValueError(f"cannot parse datetime value: {value}")

    class Meta:
        model = Event
        fields = ["key", "event_name"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    readonly_fields = [
        "key",
    ]
    fields = ["key", "event_name", "default_time", "dates"]

    def save_form(self, request, form: forms.ModelForm, change):
        if not change:
            # 新規の時はuuid4をsha256にした値を設定
            form.instance.key = sha256(uuid4().bytes).hexdigest()
        return super().save_form(request, form, change)

    def save_related(self, request, form: forms.ModelForm, formsets, change: bool):
        edited_dates_set = form.cleaned_data["dates"]

        # すでに登録済みの日付集合
        already_set_dates_set = set()

        # 登録済みで編集後に消されているものは消す
        for eventdate in form.instance.eventdate_set.all():
            if eventdate.start_datetime not in edited_dates_set:
                eventdate.delete()
            else:
                already_set_dates_set.add(eventdate.start_datetime)

        # すでに登録済みでないものだけ登録する
        for date_value in edited_dates_set:
            if date_value not in already_set_dates_set:
                event_date = EventDate(start_datetime=date_value)
                form.instance.eventdate_set.add(event_date, bulk=False)

        return super().save_related(request, form, formsets, change)
