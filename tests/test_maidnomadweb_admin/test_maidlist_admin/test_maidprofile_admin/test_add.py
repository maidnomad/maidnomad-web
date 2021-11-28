import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def add_soup(client_superuser_loggedin):
    response = client_superuser_loggedin.get(
        "/__django_admin/maidlist/maidprofile/add/",
    )
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_MarkDownエディタの表示をカスタマイズするスクリプトが出ていること(add_soup):
    tag = add_soup.select_one("script#customize-mdeditor-options")
    assert tag is not None


@pytest.mark.django_db
def test_メイドさんの登録が行えること(client_superuser_loggedin):
    response = client_superuser_loggedin.get_and_submit(
        "/__django_admin/maidlist/maidprofile/add/",
        selector="form#maidprofile_form",
        data={
            "code": "maidchan1",
            "name": "メイドちゃん",
            "description": "こんにちは♡メイドちゃんだよ！",
            "content": "## みんなへのメッセージ\nこんにちは♡メイドちゃんだよ！",
            "_save": "保存",
        },
    )
    from apps.maidlist.models import MaidProfile

    maidchan = MaidProfile.objects.get(code="maidchan1")
    assert maidchan.name == "メイドちゃん"
    assert maidchan.description == "こんにちは♡メイドちゃんだよ！"
    assert maidchan.content == "## みんなへのメッセージ\nこんにちは♡メイドちゃんだよ！"
    assert response.request["PATH_INFO"] == "/__django_admin/maidlist/maidprofile/"
