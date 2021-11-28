import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def index_soup(client_superuser_loggedin):
    response = client_superuser_loggedin.get(
        "/__django_admin/organizerlist/", follow=True
    )
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_indexページにはイベントオーガナイザープロフィール欄があること(index_soup):
    tag = index_soup.select_one(".model-organizerprofile th a")
    assert tag.text == "イベントオーガナイザー自己紹介"
    assert tag["href"] == "/__django_admin/organizerlist/organizerprofile/"
