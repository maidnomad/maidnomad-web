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
def test_jsonインポート機能を使ってオーガナイザープロフィールを登録できること(import_soup, client_superuser_loggedin):
    csv_id = {
        tag.text: tag.get("value")
        for tag in import_soup.select("select[name=input_format] option")
    }["json"]

    file = SimpleUploadedFile(
        "test.json",
        json.dumps(
            [
                {"code": "orgtaro", "name": "太郎", "order": 10, "content": "よろしく"},
                {"code": "orgjiro", "name": "次郎", "order": 20, "content": "おねがいします"},
            ]
        ).encode("utf-8"),
    )

    response = client_superuser_loggedin.submit_from_soup(
        "/__django_admin/organizerlist/organizerprofile/import/",
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
    from apps.organizerlist.models import OrganizerProfile

    data = list(
        OrganizerProfile.objects.values_list("code", "name", "order", "content")
    )
    assert data == [
        ("orgtaro", "太郎", 10, "よろしく"),
        ("orgjiro", "次郎", 20, "おねがいします"),
    ]
