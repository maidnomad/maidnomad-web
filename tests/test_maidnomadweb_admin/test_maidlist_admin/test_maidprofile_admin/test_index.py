import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def index_soup(client_superuser_loggedin):
    from factories.maidlist import MaidProfileFactory

    MaidProfileFactory(pk=101, code="maidchan", name="メイドちゃん", order=20, visible=True)
    MaidProfileFactory(pk=102, code="maidsan", name="メイドさん", order=10, visible=True)
    MaidProfileFactory(pk=103, code="maidsama", name="メイドさま", order=30, visible=True)

    response = client_superuser_loggedin.get(
        "/__django_admin/maidlist/maidprofile/", follow=True
    )
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_indexページには登録されたメイドさんが順番通りにリストされていること(index_soup):
    links = index_soup.select("table#result_list tbody a")
    assert [link.get("href") for link in links] == [
        "/__django_admin/maidlist/maidprofile/102/change/",
        "/__django_admin/maidlist/maidprofile/101/change/",
        "/__django_admin/maidlist/maidprofile/103/change/",
    ]
    assert [link.text for link in links] == [
        "メイドさん (maidsan)",
        "メイドちゃん (maidchan)",
        "メイドさま (maidsama)",
    ]


@pytest.mark.django_db
def test_indexページにはメイドさん自己紹介を追加ボタンがあること(index_soup):
    tag = index_soup.select_one("div#content .object-tools a.addlink")
    assert tag["href"] == "/__django_admin/maidlist/maidprofile/add/"


@pytest.mark.django_db
def test_indexページにはメイドさん自己紹介を追加ボタンを追加に書き換えるスクリプトがあること(index_soup):
    tags = index_soup.select_one("script#replace-add-button-text")
    assert tags.text == ('django.jQuery(".object-tools .addlink").text("追加")')


@pytest.mark.django_db
def test_indexページにはインポートボタンがあること(index_soup):
    tag = index_soup.select_one("div#content .object-tools a.import_link")
    assert tag["href"] == "/__django_admin/maidlist/maidprofile/import/"
    assert tag.text == "インポート"


@pytest.mark.django_db
def test_indexページにはエクスポートアクションのセレクトがあること(index_soup):
    tag = index_soup.select_one("select[name=action] option[value=export_admin_action]")
    assert tag.text == "選択した メイドさん自己紹介 をエクスポート"


@pytest.mark.django_db
def test_エクスポートアクションを実行するとJSONがダウンロードされること(index_soup, client_superuser_loggedin):
    json_id = {
        tag.text: tag.get("value")
        for tag in index_soup.select("select[name=file_format] option")
    }["json"]

    response = client_superuser_loggedin.submit_from_soup(
        "/__django_admin/maidlist/maidprofile/",
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
    assert [
        {key: value for key, value in data.items() if key in ["code", "name", "order"]}
        for data in json_data
    ] == [
        {"code": "maidsan", "name": "メイドさん", "order": 10},
        {"code": "maidchan", "name": "メイドちゃん", "order": 20},
        {"code": "maidsama", "name": "メイドさま", "order": 30},
    ]


@pytest.mark.django_db
def test_エクスポートアクションを実行するとCSVがダウンロードされること(index_soup, client_superuser_loggedin):
    csv_id = {
        tag.text: tag.get("value")
        for tag in index_soup.select("select[name=file_format] option")
    }["csv"]

    response = client_superuser_loggedin.submit_from_soup(
        "/__django_admin/maidlist/maidprofile/",
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
