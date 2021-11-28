import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def add_soup(client_superuser_loggedin):
    response = client_superuser_loggedin.get(
        "/__django_admin/organizerlist/organizerprofile/add/",
    )
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_MarkDownエディタの表示をカスタマイズするスクリプトが出ていること(add_soup):
    tag = add_soup.select_one("script#customize-mdeditor-options")
    assert tag is not None


@pytest.mark.django_db
def test_イベントオーガナイザーの登録が行えること(client_superuser_loggedin):
    response = client_superuser_loggedin.get_and_submit(
        "/__django_admin/organizerlist/organizerprofile/add/",
        selector="form#organizerprofile_form",
        data={
            "code": "orgtaro1",
            "name": "オーガナイザー太郎",
            "description": "初めまして！オーガナイザー太郎です！",
            "content": "## みんなへのメッセージ\n初めまして！オーガナイザー太郎です！",
            "_save": "保存",
        },
    )
    from apps.organizerlist.models import OrganizerProfile

    orgtaro = OrganizerProfile.objects.get(code="orgtaro1")
    assert orgtaro.name == "オーガナイザー太郎"
    assert orgtaro.description == "初めまして！オーガナイザー太郎です！"
    assert orgtaro.content == "## みんなへのメッセージ\n初めまして！オーガナイザー太郎です！"
    assert (
        response.request["PATH_INFO"]
        == "/__django_admin/organizerlist/organizerprofile/"
    )
