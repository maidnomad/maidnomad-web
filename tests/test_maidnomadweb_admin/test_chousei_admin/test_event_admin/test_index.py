import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def index_soup(client_superuser_loggedin):
    from factories.chousei import EventFactory

    EventFactory(pk=102, event_name="催し12")
    EventFactory(pk=101, event_name="イベント1")
    EventFactory(pk=103, event_name="いべんと123")

    response = client_superuser_loggedin.get(
        "/__django_admin/chousei/event/", follow=True
    )
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_indexページには登録されたイベントがID順にリストされていること(index_soup):
    links = index_soup.select("table#result_list tbody a")
    assert [link.get("href") for link in links] == [
        "/__django_admin/chousei/event/101/change/",
        "/__django_admin/chousei/event/102/change/",
        "/__django_admin/chousei/event/103/change/",
    ]
    assert [link.text for link in links] == [
        "イベント1",
        "催し12",
        "いべんと123",
    ]


@pytest.mark.django_db
def test_indexページにはイベント追加ボタンがあること(index_soup):
    tag = index_soup.select_one("div#content .object-tools a.addlink")
    assert tag["href"] == "/__django_admin/chousei/event/add/"
