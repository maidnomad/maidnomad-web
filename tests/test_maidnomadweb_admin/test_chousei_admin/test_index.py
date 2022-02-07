import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def index_soup(client_superuser_loggedin):
    response = client_superuser_loggedin.get("/__django_admin/chousei/", follow=True)
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_indexページにはイベント欄があること(index_soup):
    tag = index_soup.select_one(".model-event th a")
    assert tag.text == "イベント"
    assert tag["href"] == "/__django_admin/chousei/event/"
