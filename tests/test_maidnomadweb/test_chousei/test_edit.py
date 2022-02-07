import pytest
from helper import tokyo_datetime


@pytest.mark.django_db
def test_キーが存在しない時は404を返すこと(client):
    response = client.get("/chousei/foobar/edit/1")
    assert response.status_code == 404


@pytest.mark.django_db
def test_EventPersonIDが別のイベントに紐づいている時は404を返すこと(client):
    # arrange
    from factories.chousei import EventFactory, EventPersonFactory

    event1 = EventFactory()
    event2 = EventFactory()
    event2_person = EventPersonFactory(event=event2)

    # act
    response = client.get(f"/chousei/{event1.key}/edit/{event2_person.pk}")
    assert response.status_code == 404


@pytest.mark.django_db
def test_キーおよびEventPersonが存在する時は200を返すこと(client):
    # arrange
    from factories.chousei import EventFactory, EventPersonFactory

    event = EventFactory(event_name="テストイベントAAA", memo="めめめ")
    event_person = EventPersonFactory(event=event)

    # act
    response = client.get(f"/chousei/{event.key}/edit/{event_person.pk}")

    # assert
    assert response.status_code == 200
    assert response.context["event"].event_name == "テストイベントAAA"
    assert response.context["event"].memo == "めめめ"


@pytest.mark.django_db
def test_Eventに紐づくEventDateを入力するフォームを構築できていること(client):
    # arrange
    from factories.chousei import (
        EventDateFactory,
        EventFactory,
        EventPersonFactory,
        ScheduleFactory,
    )

    event1 = EventFactory()
    event2 = EventFactory()
    event_person = EventPersonFactory(event=event1, name="参加太郎")
    # 日付は登録順に依存せず実際の日付順になることを確かめるためあえて順番をばらす
    date_1223 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 2, 23, 0)
    )
    date_1101 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 1, 1, 0)
    )
    date_1216 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 2, 16, 0)
    )
    EventDateFactory(
        event=event2, start_datetime=tokyo_datetime(2021, 12, 31, 1, 0)
    )  # 結果に含まない
    ScheduleFactory(event_person=event_person, event_date=date_1101, answer=0)
    ScheduleFactory(event_person=event_person, event_date=date_1216, answer=2)
    ScheduleFactory(event_person=event_person, event_date=date_1223, answer=1)

    # act
    response = client.get(f"/chousei/{event1.key}/edit/{event_person.pk}")

    # assert
    assert response.status_code == 200
    assert response.context["person"].name == "参加太郎"
    form = response.context["form"]
    assert [field.label for field in form.schedule_answer_fields()] == [
        "2022/01/01(土) 01:00",
        "2022/01/02(日) 16:00",
        "2022/01/02(日) 23:00",
    ]
    assert [field.name for field in form.schedule_answer_fields()] == [
        f"eventdate_{date_1101.pk}",
        f"eventdate_{date_1216.pk}",
        f"eventdate_{date_1223.pk}",
    ]
    assert [field.widget_type for field in form.schedule_answer_fields()] == [
        "radioselect",
        "radioselect",
        "radioselect",
    ]
    assert [field.field.choices for field in form.schedule_answer_fields()] == [
        [(0, "×"), (1, "△"), (2, "○")],
        [(0, "×"), (1, "△"), (2, "○")],
        [(0, "×"), (1, "△"), (2, "○")],
    ]
    assert [field.value() for field in form.schedule_answer_fields()] == [0, 2, 1]


@pytest.mark.django_db
def test_フォーム項目に不備があるとバリデーションが働くこと(client):
    # arrange
    from factories.chousei import (
        EventDateFactory,
        EventFactory,
        EventPersonFactory,
    )

    event1 = EventFactory(event_name="ほげほげ会議")
    date_1101 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 1, 1, 0)
    )
    event_person = EventPersonFactory(event=event1, name="名前なまえ")

    # act
    response = client.post(
        f"/chousei/{event1.key}/edit/{event_person.pk}",
        {
            "name": "",
        },
        follow=True,
    )

    # assert
    assert response.status_code == 200
    assert response.context["form"].errors == {
        "name": ["このフィールドは必須です。"],
        "eventdate_1": ["このフィールドは必須です。"],
    }
    # データが登録されていないこと
    from apps.chousei.models import EventPerson, Schedule

    assert EventPerson.objects.get(pk=event_person.pk).name == "名前なまえ"
    assert Schedule.objects.count() == 0


@pytest.mark.django_db
def test_フォームに値を入力して登録するとデータが追加されること(client):
    # arrange
    from factories.chousei import (
        EventDateFactory,
        EventFactory,
        EventPersonFactory,
        ScheduleFactory,
    )

    event1 = EventFactory(event_name="ほげほげ会議1")
    event_person = EventPersonFactory(
        event=event1,
        name="さんかしゃ変更前",
        comment="コメント変更前",
    )
    date_1101 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 1, 1, 0)
    )
    date_1216 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 2, 16, 0)
    )
    date_1223 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 2, 23, 0)
    )
    ScheduleFactory(event_person=event_person, event_date=date_1216, answer=1)
    ScheduleFactory(event_person=event_person, event_date=date_1223, answer=0)

    # act
    response = client.post(
        f"/chousei/{event1.key}/edit/{event_person.pk}",
        {
            "name": "さんかしゃ名前変更後",
            f"eventdate_{date_1101.pk}": 0,
            f"eventdate_{date_1216.pk}": 1,
            f"eventdate_{date_1223.pk}": 2,
            "comment": "コメント変更後",
        },
        follow=True,
    )

    # assert
    assert response.status_code == 200

    from apps.chousei.models import EventPerson, Schedule

    assert list(
        EventPerson.objects.values_list("event__event_name", "name", "comment")
    ) == [("ほげほげ会議1", "さんかしゃ名前変更後", "コメント変更後")]
    assert list(
        Schedule.objects.values_list(
            "event_person__name", "event_date__start_datetime", "answer"
        ).order_by("event_date__start_datetime")
    ) == [
        ("さんかしゃ名前変更後", tokyo_datetime(2022, 1, 1, 1, 0), 0),
        ("さんかしゃ名前変更後", tokyo_datetime(2022, 1, 2, 16, 0), 1),
        ("さんかしゃ名前変更後", tokyo_datetime(2022, 1, 2, 23, 0), 2),
    ]
