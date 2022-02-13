import pytest
from helper import tokyo_datetime


@pytest.mark.django_db
def test_キーが存在しない時は404を返すこと(client):
    response = client.get("/chousei/foobar")
    assert response.status_code == 404


@pytest.mark.django_db
def test_キーが存在する時は200を返すこと(client):
    # arrange
    from factories.chousei import EventFactory

    event = EventFactory(event_name="テストイベント012", memo="めもめも")

    # act
    response = client.get(f"/chousei/{event.key}")

    # assert
    assert response.status_code == 200
    assert response.context["event"].event_name == "テストイベント012"
    assert response.context["event"].memo == "めもめも"


@pytest.mark.django_db
def test_Eventに紐づくEventPersonを取得していること(client):
    # arrange
    from factories.chousei import EventFactory, EventPersonFactory

    event1 = EventFactory()
    event2 = EventFactory()
    EventPersonFactory(event=event1, name="参加者1", comment="コメコメ")
    EventPersonFactory(event=event1, name="参加者2")
    EventPersonFactory(event=event1, name="参加者3")
    EventPersonFactory(event=event2, name="参加者4")  # 結果に含まない

    # act
    response = client.get(f"/chousei/{event1.key}")

    # assert
    assert response.status_code == 200
    assert [
        (event_person.name, event_person.comment)
        for event_person in response.context["event_people"]
    ] == [("参加者1", "コメコメ"), ("参加者2", ""), ("参加者3", "")]


@pytest.mark.django_db
def test_Eventに紐づくevent_date_answerを取得していること(client):
    # arrange
    from factories.chousei import (
        EventDateFactory,
        EventFactory,
        EventPersonFactory,
        ScheduleFactory,
    )

    event1 = EventFactory()
    event2 = EventFactory()
    # 日付は登録順に依存せず実際の日付順になることを確かめるためあえて逆順に登録する
    date_2100 = EventDateFactory(
        event=event2, start_datetime=tokyo_datetime(2022, 2, 1, 0, 0)
    )  # 結果に含まない
    date_1217 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 2, 17, 0)
    )
    date_1216 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 2, 16, 0)
    )
    date_1115 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 1, 15, 0)
    )
    person1 = EventPersonFactory(event=event1, name="参加者1", comment="コメコメ")
    person2 = EventPersonFactory(event=event1, name="参加者2")
    person3 = EventPersonFactory(event=event2, name="参加者3")  # 結果に含まない
    ScheduleFactory(event_person=person1, event_date=date_1115, answer=0)
    ScheduleFactory(event_person=person1, event_date=date_1216, answer=1)
    ScheduleFactory(event_person=person1, event_date=date_1217, answer=2)
    ScheduleFactory(event_person=person2, event_date=date_1115, answer=1)
    ScheduleFactory(event_person=person2, event_date=date_1216, answer=2)
    ScheduleFactory(event_person=person2, event_date=date_1217, answer=0)
    ScheduleFactory(event_person=person3, event_date=date_2100, answer=2)

    # act
    response = client.get(f"/chousei/{event1.key}")

    # assert
    assert response.status_code == 200
    assert response.context["event_date_answer_list"] == [
        {
            "start_datetime": tokyo_datetime(2022, 1, 1, 15, 0),
            "answer_list": ["×", "△"],
        },
        {
            "start_datetime": tokyo_datetime(2022, 1, 2, 16, 0),
            "answer_list": ["△", "○"],
        },
        {
            "start_datetime": tokyo_datetime(2022, 1, 2, 17, 0),
            "answer_list": ["○", "×"],
        },
    ]
