import pytest


@pytest.mark.django_db
def test_メイドカフェ様向けノマド会紹介のレスポンスが仕様通りであること(client, settings):
    # fmt: off
    # arrange
    settings.SITE_ROOT_URL = "https://example.com"
    # act
    response = client.get("/information/maidnomad_info")
    content = response.content.decode("UTF-8")

    # assert
    assert response.status_code == 200
    assert "<title>メイドカフェ店舗様向けノマド会のご紹介 | メイドカフェでノマド会公式サイト</title>" in content
    assert '<meta property="og:site_name" content="メイドカフェでノマド会公式サイト" />' in content
    assert '<meta property="og:title" content="メイドカフェ店舗様向けノマド会のご紹介" />' in content
    assert '<meta property="og:type" content="article" />' in content
    assert '<meta name="description" content="メイドカフェ様向けに私達メイドカフェでノマド会の目指していること、一緒に取り組んでいきたいことを説明する資料を掲載しています。" />' in content
    assert '<meta property="og:description" content="メイドカフェ様向けに私達メイドカフェでノマド会の目指していること、一緒に取り組んでいきたいことを説明する資料を掲載しています。" />' in content
    assert '<link rel="canonical" href="https://example.com/information/maidnomad_info" />' in content
    # bookmark
    assert '//b.hatena.ne.jp/entry/https://example.com/information/maidnomad_info' in content
