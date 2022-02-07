import pytest
from bs4 import BeautifulSoup
from helper import tokyo_datetime


@pytest.fixture
def event1():
    from factories.chousei import EventFactory

    event = EventFactory(event_name="変更前のイベント名", memo="変更前のメモ")
    return event


@pytest.fixture
def event_date1(event1):
    from factories.chousei import EventDateFactory

    return EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 2, 2, 12, 45)
    )


@pytest.fixture
def edit_soup(client_superuser_loggedin, event1):
    response = client_superuser_loggedin.get(
        f"/__django_admin/chousei/event/{event1.pk}/change/",
    )
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_イベントの更新が行えること(client_superuser_loggedin, event1, event_date1):
    from factories.chousei import EventDateFactory

    # 消される時刻
    event_date_to_remove = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2021, 12, 31, 1, 0)
    )

    response = client_superuser_loggedin.get_and_submit(
        f"/__django_admin/chousei/event/{event1.pk}/change/",
        selector="form#event_form",
        data={
            "event_name": "変更したイベント名",
            "memo": "変更後のメモ",
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
 
    from apps.chousei.models import Event, EventDate

    updated_event = Event.objects.get(pk=event1.pk)
    assert updated_event.event_name == "変更したイベント名"
    assert updated_event.memo == "変更後のメモ"
    assert list(
        updated_event.eventdate_set.values_list(
            "start_datetime",
            flat=True,
        ).order_by("start_datetime")
    ) == [
        tokyo_datetime(2022, 2, 1, 8, 0),
        tokyo_datetime(2022, 2, 2, 12, 45),
        tokyo_datetime(2022, 2, 3, 20, 30),
    ]
    # 元々あったEventDateは消えずにそのままであること
    assert EventDate.objects.filter(pk=event_date1.pk).exists()
    # 登録されてない時刻は消されていること
    assert not EventDate.objects.filter(pk=event_date_to_remove.pk).exists()

