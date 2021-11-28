import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def index_soup(client_superuser_loggedin):
    response = client_superuser_loggedin.get("/__django_admin/maidlist/", follow=True)
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_indexページにはメイドさんプロフィール欄があること(index_soup):
    tag = index_soup.select_one(".model-maidprofile th a")
    assert tag.text == "メイドさん自己紹介"
    assert tag["href"] == "/__django_admin/maidlist/maidprofile/"
