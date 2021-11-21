import pytest


@pytest.mark.django_db
def test_メイドカフェ紹介のレスポンスが仕様通りであること(client, settings):
    # fmt: off
    # arrange
    settings.SITE_ROOT_URL = "https://example.com"
    # act
    response = client.get("/information/maidcafe_info")
    content = response.content.decode("UTF-8")

    # assert
    assert response.status_code == 200
    assert "<title>ノマドができるメイドカフェ紹介 | メイドカフェでノマド会公式サイト</title>" in content
    assert '<meta property="og:site_name" content="メイドカフェでノマド会公式サイト" />' in content
    assert '<meta property="og:title" content="ノマドができるメイドカフェ紹介" />' in content
    assert '<meta property="og:type" content="article" />' in content
    assert '<meta name="description" content="どのお店に行けば良いのかまったく分からないという方のために、メイドカフェでノマド会としておすすめのお店を紹介します。" />' in content
    assert '<meta property="og:description" content="どのお店に行けば良いのかまったく分からないという方のために、メイドカフェでノマド会としておすすめのお店を紹介します。" />' in content
    assert '<link rel="canonical" href="https://example.com/information/maidcafe_info" />' in content
    # bookmark
    assert '//b.hatena.ne.jp/entry/https://example.com/information/maidcafe_info' in content
