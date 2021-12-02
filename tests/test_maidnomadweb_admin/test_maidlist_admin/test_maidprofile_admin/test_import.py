import json

import pytest
from bs4 import BeautifulSoup
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def import_soup(client_superuser_loggedin):
    response = client_superuser_loggedin.get(
        "/__django_admin/organizerlist/organizerprofile/import/", follow=True
    )
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_jsonインポート機能を使ってメイドプロフィールを登録できること(import_soup, client_superuser_loggedin):
    csv_id = {
        tag.text: tag.get("value")
        for tag in import_soup.select("select[name=input_format] option")
    }["json"]

    file = SimpleUploadedFile(
        "test.json",
        json.dumps(
            [
                {"code": "maidsan", "name": "メイドさん", "order": 10, "content": "おはよう"},
                {"code": "maidchan", "name": "メイドちゃん", "order": 20, "content": "おやすみ"},
            ]
        ).encode("utf-8"),
    )

    response = client_superuser_loggedin.submit_from_soup(
        "/__django_admin/maidlist/maidprofile/import/",
        import_soup,
        selector="#content form",
        data={
            "import_file": file,
            "input_format": csv_id,
            "_save": "確定",
        },
    )

    # 確認画面
    confirm_soup = BeautifulSoup(response.content, "html.parser")
    response = client_superuser_loggedin.submit_from_soup(
        "",
        confirm_soup,
        selector="#content form",
        data={"confirm": "インポート実行"},
    )

    # assert
    from apps.maidlist.models import MaidProfile

    data = list(MaidProfile.objects.values_list("code", "name", "order", "content"))
    assert data == [
        ("maidsan", "メイドさん", 10, "おはよう"),
        ("maidchan", "メイドちゃん", 20, "おやすみ"),
    ]
