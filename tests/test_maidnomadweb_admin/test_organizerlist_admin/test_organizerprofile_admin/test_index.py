import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def index_soup(client_superuser_loggedin):
    from factories.organizerlist import OrganizerProfileFactory

    OrganizerProfileFactory(
        pk=101, code="orgtaro", name="オーガナイザー太郎", order=20, visible=True
    )
    OrganizerProfileFactory(
        pk=102, code="orgjiro", name="オーガナイザー次郎", order=10, visible=True
    )
    OrganizerProfileFactory(
        pk=103, code="orgsaburo", name="オーガナイザー三郎", order=30, visible=True
    )

    response = client_superuser_loggedin.get(
        "/__django_admin/organizerlist/organizerprofile/", follow=True
    )
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_indexページには登録されたイベントオーガナイザーが順番通りにリストされていること(index_soup):
    links = index_soup.select("table#result_list tbody a")
    assert [link.get("href") for link in links] == [
        "/__django_admin/organizerlist/organizerprofile/102/change/",
        "/__django_admin/organizerlist/organizerprofile/101/change/",
        "/__django_admin/organizerlist/organizerprofile/103/change/",
    ]
    assert [link.text for link in links] == [
        "オーガナイザー次郎 (orgjiro)",
        "オーガナイザー太郎 (orgtaro)",
        "オーガナイザー三郎 (orgsaburo)",
    ]


@pytest.mark.django_db
def test_indexページにはイベントオーガナイザー自己紹介を追加ボタンがあること(index_soup):
    tag = index_soup.select_one("div#content .object-tools a.addlink")
    assert tag["href"] == "/__django_admin/organizerlist/organizerprofile/add/"


@pytest.mark.django_db
def test_indexページにはオーガナイザー次郎自己紹介を追加ボタンを追加に書き換えるスクリプトがあること(index_soup):
    tags = index_soup.select_one("script#replace-add-button-text")
    assert tags.text == ('django.jQuery(".object-tools .addlink").text("追加")')


@pytest.mark.django_db
def test_indexページにはインポートボタンがあること(index_soup):
    tag = index_soup.select_one("div#content .object-tools a.import_link")
    assert tag["href"] == "/__django_admin/organizerlist/organizerprofile/import/"
    assert tag.text == "インポート"


@pytest.mark.django_db
def test_indexページにはエクスポートアクションのセレクトがあること(index_soup):
    tag = index_soup.select_one("select[name=action] option[value=export_admin_action]")
    assert tag.text == "選択した イベントオーガナイザー自己紹介 をエクスポート"


@pytest.mark.django_db
def test_エクスポートアクションを実行するとJSONがダウンロードされること(index_soup, client_superuser_loggedin):
    json_id = {
        tag.text: tag.get("value")
        for tag in index_soup.select("select[name=file_format] option")
    }["json"]

    response = client_superuser_loggedin.submit_from_soup(
        "/__django_admin/organizerlist/organizerprofile/",
        index_soup,
        selector="form#changelist-form",
        data={
            "action": "export_admin_action",
            "file_format": json_id,
            "_selected_action": ["101", "102", "103"],
        },
    )

    json_data = response.json()
    assert len(json_data) == 3
    assert set(json_data[0].keys()) == {
        "code",
        "name",
        "description",
        "content",
        "thumbnail_image",
        "main_image",
        "og_image",
        "visible",
        "order",
    }


@pytest.mark.django_db
def test_エクスポートアクションを実行するとCSVがダウンロードされること(index_soup, client_superuser_loggedin):
    csv_id = {
        tag.text: tag.get("value")
        for tag in index_soup.select("select[name=file_format] option")
    }["csv"]

    response = client_superuser_loggedin.submit_from_soup(
        "/__django_admin/organizerlist/organizerprofile/",
        index_soup,
        selector="form#changelist-form",
        data={
            "action": "export_admin_action",
            "file_format": csv_id,
            "_selected_action": ["101", "102", "103"],
        },
    )

    csv_text = response.content.decode("utf-8")
    csv_lines = csv_text.split("\n")
    assert (
        csv_lines[0].strip()
        == "code,name,description,content,thumbnail_image,main_image,og_image,visible,order"
    )
