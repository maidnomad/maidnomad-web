import pytest


@pytest.mark.django_db
def test_組織のレスポンスが仕様通りであること(client, settings):
    # fmt: off
    # arrange
    settings.SITE_ROOT_URL = "https://example.com"
    # act
    response = client.get("/organization")
    content = response.content.decode("UTF-8")

    # assert
    assert response.status_code == 200
    assert "<title>運営体制 | メイドカフェでノマド会公式サイト</title>" in content
    assert '<meta property="og:site_name" content="メイドカフェでノマド会公式サイト" />' in content
    assert '<meta property="og:title" content="運営体制" />' in content
    assert '<meta property="og:type" content="article" />' in content
    assert '<meta name="description" content="メイドカフェでノマド会の運営体制と参加者、イベントオーガナイザー、メイドさんの役割を説明します。" />' in content
    assert '<meta property="og:description" content="メイドカフェでノマド会の運営体制と参加者、イベントオーガナイザー、メイドさんの役割を説明します。" />' in content
    assert '<link rel="canonical" href="https://example.com/organization" />' in content
    # bookmark
    assert '//b.hatena.ne.jp/entry/https://example.com/organization' in content
