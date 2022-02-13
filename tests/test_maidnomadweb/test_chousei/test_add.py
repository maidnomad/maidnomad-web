import pytest
from helper import tokyo_datetime


@pytest.mark.django_db
def test_キーが存在しない時は404を返すこと(client):
    response = client.get("/chousei/foobar/add")
    assert response.status_code == 404


@pytest.mark.django_db
def test_キーが存在する時は200を返すこと(client):
    # arrange
    from factories.chousei import EventFactory

    event = EventFactory(event_name="テストイベントXYZ", memo="めもめもめ")

    # act
    response = client.get(f"/chousei/{event.key}/add")

    # assert
    assert response.status_code == 200
    assert response.context["event"].event_name == "テストイベントXYZ"
    assert response.context["event"].memo == "めもめもめ"


@pytest.mark.django_db
def test_Eventに紐づくEventDateを入力するフォームを構築できていること(client):
    # arrange
    from factories.chousei import EventDateFactory, EventFactory

    event1 = EventFactory()
    event2 = EventFactory()
    # 日付は登録順に依存せず実際の日付順になることを確かめるためあえて逆順に登録する
    date_1223 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 2, 23, 0)
    )
    date_1216 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 2, 16, 0)
    )
    date_1101 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 1, 1, 0)
    )
    EventDateFactory(
        event=event2, start_datetime=tokyo_datetime(2021, 12, 31, 1, 0)
    )  # 結果に含まない

    # act
    response = client.get(f"/chousei/{event1.key}/add")

    # assert
    assert response.status_code == 200
    assert "person" not in response.context
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
        [(2, "○"), (1, "△"), (0, "×")],
        [(2, "○"), (1, "△"), (0, "×")],
        [(2, "○"), (1, "△"), (0, "×")],
    ]


@pytest.mark.django_db
def test_フォーム項目に不備があるとバリデーションが働くこと(client):
    # arrange
    from factories.chousei import EventDateFactory, EventFactory

    event1 = EventFactory(event_name="ほげほげ会議")
    EventDateFactory(event=event1, start_datetime=tokyo_datetime(2022, 1, 1, 1, 0))

    # act
    response = client.post(
        f"/chousei/{event1.key}/add",
        {
            "name": "",
        },
        follow=True,
    )

    # assert
    assert response.status_code == 200
    assert response.context["form"].errors == {
        "name": ["名前を入力してください"],
        "eventdate_1": ["回答を選んでください"],
    }
    # データが登録されていないこと
    from apps.chousei.models import EventPerson, Schedule

    assert EventPerson.objects.count() == 0
    assert Schedule.objects.count() == 0


@pytest.mark.django_db
def test_フォームに値を入力して登録するとデータが追加されること(client, mock_post_to_slack):
    # arrange
    from factories.chousei import EventDateFactory, EventFactory

    event1 = EventFactory(
        event_name="ほげほげ会議", slack_notification_user="@hogehogeuser, #somechannel"
    )
    event2 = EventFactory()
    # 日付は登録順に依存せず実際の日付順になることを確かめるためあえて逆順に登録する
    date_1223 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 2, 23, 0)
    )
    date_1216 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 2, 16, 0)
    )
    date_1101 = EventDateFactory(
        event=event1, start_datetime=tokyo_datetime(2022, 1, 1, 1, 0)
    )
    EventDateFactory(
        event=event2, start_datetime=tokyo_datetime(2021, 12, 31, 1, 0)
    )  # 結果に含まない

    # act
    response = client.post(
        f"/chousei/{event1.key}/add",
        {
            "name": "さんかしゃ00",
            f"eventdate_{date_1101.pk}": 0,
            f"eventdate_{date_1216.pk}": 1,
            f"eventdate_{date_1223.pk}": 2,
            "comment": "コメントこめこめ",
        },
        follow=True,
    )

    # assert
    assert response.status_code == 200

    from apps.chousei.models import EventPerson, Schedule

    assert list(
        EventPerson.objects.values_list("event__event_name", "name", "comment")
    ) == [("ほげほげ会議", "さんかしゃ00", "コメントこめこめ")]
    assert list(
        Schedule.objects.values_list(
            "event_person__name", "event_date__start_datetime", "answer"
        ).order_by("event_date__start_datetime")
    ) == [
        ("さんかしゃ00", tokyo_datetime(2022, 1, 1, 1, 0), 0),
        ("さんかしゃ00", tokyo_datetime(2022, 1, 2, 16, 0), 1),
        ("さんかしゃ00", tokyo_datetime(2022, 1, 2, 23, 0), 2),
    ]
    # Slack通知の確認
    event_url = f"http://localhost:8000/chousei/{event1.key}"
    notify_message = f"さんかしゃ00 さんが <{event_url}|ほげほげ会議> の予定を登録したよ。"
    mock_post_to_slack.assert_any_call(
        {
            "channel": "@hogehogeuser",
            "text": notify_message,
        },
        log_name="event_schedule_added",
        log_channel="@hogehogeuser",
    )
    mock_post_to_slack.assert_any_call(
        {
            "channel": "#somechannel",
            "text": notify_message,
        },
        log_name="event_schedule_added",
        log_channel="#somechannel",
    )
