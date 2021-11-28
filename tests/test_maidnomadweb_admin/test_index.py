import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def index_soup(client_superuser_loggedin):
    response = client_superuser_loggedin.get("/__django_admin/", follow=True)
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_indexページにはメイドさんリストへのリンクがあること(index_soup):
    tag = index_soup.select_one("div.app-maidlist a.section")
    assert tag.text == "メイドさんリスト"
    assert tag["href"] == "/__django_admin/maidlist/"


@pytest.mark.django_db
def test_indexページにはメイドさんプロフィールリストへのリンクがあること(index_soup):
    tag = index_soup.select_one("div.app-maidlist a.section")
    assert tag.text == "メイドさんリスト"
    assert tag["href"] == "/__django_admin/maidlist/"


@pytest.mark.django_db
def test_indexページにはイベントオーガナイザーリストへのリンクがあること(index_soup):
    tag = index_soup.select_one("div.app-organizerlist a.section")
    assert tag.text == "イベントオーガナイザーリスト"
    assert tag["href"] == "/__django_admin/organizerlist/"
