import pytest
from helper import tokyo_datetime


@pytest.mark.django_db
def test_イベントの登録が行えること(client_superuser_loggedin):
    response = client_superuser_loggedin.get_and_submit(
        "/__django_admin/chousei/event/add/",
        selector="form#event_form",
        data={
            "event_name": "追加したイベント名",
            "memo": "メモメモメモめ",
            "default_time": "8:00",
            "dates": """
2022/02/01
2022/02/02 12:45

2022/02/03 20:30
""",
            "_save": "保存",
        },
    )
    assert response.request["PATH_INFO"] == "/__django_admin/chousei/event/"

    from apps.chousei.models import Event

    event = Event.objects.get(event_name="追加したイベント名")
    assert event.memo == "メモメモメモめ"
    assert list(
        event.eventdate_set.values_list(
            "start_datetime",
            flat=True,
        ).order_by("start_datetime")
    ) == [
        tokyo_datetime(2022, 2, 1, 8, 0),
        tokyo_datetime(2022, 2, 2, 12, 45),
        tokyo_datetime(2022, 2, 3, 20, 30),
    ]


@pytest.mark.django_db
def test_デフォルト時刻が設定されていない時は時刻の入力が必須であること(client_superuser_loggedin):
    response = client_superuser_loggedin.get_and_submit(
        "/__django_admin/chousei/event/add/",
        selector="form#event_form",
        data={
            "event_name": "追加したイベント名",
            "memo": "メモメモメモめ",
            "default_time": "",
            "dates": """
2022/02/01
2022/02/02 12:45

2022/02/03 20:30
""",
            "_save": "保存",
        },
    )
    assert response.context_data["adminform"].errors == {
        "dates": ["日付のフォーマットが不正です 2022/02/01"]
    }


@pytest.mark.django_db
def test_デフォルト時刻が設定されて値が不正の時はエラーメッセージを表示すること(client_superuser_loggedin):
    response = client_superuser_loggedin.get_and_submit(
        "/__django_admin/chousei/event/add/",
        selector="form#event_form",
        data={
            "event_name": "追加したイベント名",
            "memo": "メモメモメモめ",
            "default_time": "XXXX",
            "dates": """
2022/02/01 08:00
""",
            "_save": "保存",
        },
    )
    assert response.context_data["adminform"].errors == {
        "default_time": ["時刻のフォーマットは HH:MM 形式で入力してください"]
    }


@pytest.mark.django_db
def test_日付値が不正の時はエラーメッセージを表示すること(client_superuser_loggedin):
    response = client_superuser_loggedin.get_and_submit(
        "/__django_admin/chousei/event/add/",
        selector="form#event_form",
        data={
            "event_name": "追加したイベント名",
            "memo": "メモメモメモめ",
            "default_time": "12:00",
            "dates": """
2022/02/31 08:00
""",
            "_save": "保存",
        },
    )
    assert response.context_data["adminform"].errors == {
        "dates": ["日付のフォーマットが不正です 2022/02/31 08:00"]
    }
