import pytest


@pytest.mark.django_db
def test_トップページのレスポンスが仕様通りであること(client, settings):
    # fmt: off
    # arrange
    settings.SITE_ROOT_URL = "https://example.com"
    # act
    response = client.get("/")
    content = response.content.decode("UTF-8")

    # assert
    assert response.status_code == 200
    assert "<title>メイドカフェでノマド会公式サイト</title>" in content
    assert '<meta property="og:site_name" content="メイドカフェでノマド会公式サイト" />' in content
    assert '<meta property="og:title" content="メイドカフェでノマド会公式ページへようこそ" />' in content
    assert '<meta property="og:type" content="website" />' in content
    assert '<meta name="description" content="メイドカフェでノマドワークの素晴らしさを世の中に広げる活動をしています。" />' in content
    assert '<meta property="og:description" content="メイドカフェでノマドワークの素晴らしさを世の中に広げる活動をしています。" />' in content
    assert '<link rel="canonical" href="https://example.com/" />' in content
    # bookmark
    assert '//b.hatena.ne.jp/entry/https://example.com/' in content
