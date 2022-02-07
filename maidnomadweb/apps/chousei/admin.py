from datetime import datetime
from hashlib import sha256
from uuid import uuid4

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Event, EventDate


DATETIME_FORMAT = "%Y/%m/%d %H:%M"


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["key", "event_name", "memo"]

    default_time = forms.CharField(label="デフォルト時刻", required=False)
    dates = forms.CharField(label="候補日時", widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._retrieve_dates_textarea()

    def _retrieve_dates_textarea(self):
        """dates テキストエリアに eventdate を展開する"""
        if self.instance.pk:
            # 更新の時のみ
            initial_dates = "\n".join(
                sorted(
                    [
                        timezone.localtime(eventdate.start_datetime).strftime(
                            DATETIME_FORMAT
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

    def _parse_datetime(self, value) -> datetime:
        """テキストエリアに入力された1行分の日付をパースする

        デフォルト時刻が設定されている場合は日付を省略した場合デフォルト時刻でパースする
        """
        try:
            return datetime.strptime(value, DATETIME_FORMAT)
        except ValueError:
            pass
        default_time = self.cleaned_data.get("default_time")
        if default_time:
            try:
                value_date = datetime.strptime(value, "%Y/%m/%d")
                value_date = datetime.combine(value_date, default_time)
                return value_date
            except ValueError:
                pass
        raise ValueError(
            f"cannot parse datetime value: {value}, default_time: {default_time}"
        )

    def set_instance_key_random(self):
        """インスタンスにランダムkeyをセットする"""
        # uuid4をsha256にした値
        self.instance.key = sha256(uuid4().bytes).hexdigest()

    def save_event_dates(self):
        """登録されたデータをもとに、instanceに紐づくEventDateを登録・更新・削除する

        以下のルールで処理を行う。
        - 登録済みで編集後に消されているものは消す
        - 登録済みで編集後にも残っているものはなにもしない
        - 編集後に存在し、登録済みでないものは新たに登録する
        """
        edited_dates_set = self.cleaned_data["dates"]

        # すでに登録済みの日付集合
        already_set_dates_set = set()

        # 登録済みで編集後に消されているものは消す
        for eventdate in self.instance.eventdate_set.all():
            if eventdate.start_datetime not in edited_dates_set:
                eventdate.delete()
            else:
                already_set_dates_set.add(eventdate.start_datetime)

        # すでに登録済みでないものだけ登録する
        for date_value in edited_dates_set:
            if date_value not in already_set_dates_set:
                event_date = EventDate(start_datetime=date_value)
                self.instance.eventdate_set.add(event_date, bulk=False)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    readonly_fields = [
        "key",
    ]
    fields = ["key", "event_name", "memo", "default_time", "dates"]

    def save_form(self, request, form: EventAdminForm, change):
        if not change:
            # 新規の時はランダムキーを生成して設定
            form.set_instance_key_random()
        return super().save_form(request, form, change)

    def save_related(self, request, form: EventAdminForm, formsets, change: bool):
        form.save_event_dates()
        return super().save_related(request, form, formsets, change)
