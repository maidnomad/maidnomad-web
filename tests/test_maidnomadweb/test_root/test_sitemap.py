from datetime import datetime
from xml.etree import ElementTree

import pytest
import pytz

NS = {"": "http://www.sitemaps.org/schemas/sitemap/0.9"}
TOKYO_TZ = pytz.timezone("Asia/Tokyo")


@pytest.mark.django_db
def test_sitemapがレスポンスを返すこと(client, settings):
    # arrange
    settings.SITE_ROOT_URL = "https://example.com"
    # act
    response = client.get("/sitemap.xml")
    content = response.content.decode("UTF-8")

    # assert
    assert response.status_code == 200

    root = ElementTree.fromstring(content)

    assert (
        root.find(".//sitemap[loc='https://example.com/sitemap_django.xml']", NS)
        is not None
    )
    assert (
        root.find(".//sitemap[loc='https://www.maid-cafe.work/sitemap-misc.xml']", NS)
        is not None
    )


@pytest.mark.django_db
def test_sitemap_djangoがトップページを含めたレスポンスを返すこと(client, settings):
    # arrange
    settings.SITE_ROOT_URL = "https://example.com"
    # act
    response = client.get("/sitemap_django.xml")
    content = response.content.decode("UTF-8")

    # assert
    assert response.status_code == 200
    root = ElementTree.fromstring(content)
    toppage_elem = root.find(".//url[loc='https://example.com/']", NS)
    assert toppage_elem.find("changefreq", NS).text == "monthly"  # type: ignore
    assert toppage_elem.find("priority", NS).text == "1.0"  # type: ignore


@pytest.mark.django_db
def test_sitemap_djangoがメイドさんの更新日付に応じたレスポンスを返すこと(client, settings):
    # arrange
    settings.SITE_ROOT_URL = "https://example.com"

    from factories import MaidProfileFactory

    maidchan = MaidProfileFactory(
        code="maidchan",
    )
    # 現在時刻はFactoryでは上書きされてしまうので無理矢理更新して設定する
    from apps.maidlist.models import MaidProfile

    MaidProfile.objects.filter(pk=maidchan.pk).update(
        updated_at=datetime(2021, 12, 1, 0, 0, 0, tzinfo=TOKYO_TZ)
    )
    # act
    response = client.get("/sitemap_django.xml")
    content = response.content.decode("UTF-8")

    # assert
    assert response.status_code == 200
    root = ElementTree.fromstring(content)
    maidpage_elem = root.find(
        ".//url[loc='https://example.com/organization/maid_profile/maidchan']",
        namespaces=NS,
    )
    assert maidpage_elem.find("changefreq", NS).text == "monthly"  # type: ignore
    assert maidpage_elem.find("priority", NS).text == "0.9"  # type: ignore
    # 東京だと9時間ずれているからUTCだと前日になっているはず
    assert maidpage_elem.find("lastmod", NS).text == "2021-11-30"  # type: ignore
