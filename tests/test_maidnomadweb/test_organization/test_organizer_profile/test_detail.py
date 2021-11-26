import pytest


@pytest.mark.django_db
class Testオーガナイザー紹介詳細ページ:
    def test_オーガナイザーの名前と画像が表示されること(self, client):
        # arrange
        from factories import OrganizerProfileFactory

        OrganizerProfileFactory(
            code="orgtaro",
            name="オーガナイザー太郎",
            main_image__filename="orgtaro.jpg",
            og_image__filename="orgtaro_og.jpg",
        )

        # act
        response = client.get("/organization/organizers_profile/orgtaro")

        # assert
        assert response.status_code == 200
        assert response.context["profile"].code == "orgtaro"
        assert response.context["profile"].name == "オーガナイザー太郎"
        assert response.context["image_url"] == "/media/organizerlist_main/orgtaro.jpg"
        assert (
            response.context["og_image_url"]
            == "/media/organizerlist_ogp/orgtaro_og.jpg"
        )

    def test_OGPが設定されていない時はサムネイル画像が表示されること(self, client):
        # arrange
        from factories import OrganizerProfileFactory

        OrganizerProfileFactory(
            code="orgtaro",
            name="オーガナイザー太郎",
            main_image__filename="orgtaro.jpg",
            thumbnail_image__filename="orgtaro.jpg",
            og_image=None,
        )

        # act
        response = client.get("/organization/organizers_profile/orgtaro")

        # assert
        assert response.status_code == 200
        assert (
            response.context["og_image_url"]
            == "/media/organizerlist_thumbnail/orgtaro.jpg"
        )

    def test_メイン画像がNullの時はサムネイル画像を表示すること(self, client):
        # arrange
        from factories import OrganizerProfileFactory

        OrganizerProfileFactory(
            code="orgtaro",
            thumbnail_image__filename="orgtaro.jpg",
            main_image=None,
            og_image=None,
        )

        # act
        response = client.get("/organization/organizers_profile/orgtaro")

        # assert
        assert response.status_code == 200
        assert (
            response.context["image_url"]
            == "/media/organizerlist_thumbnail/orgtaro.jpg"
        )
        assert (
            response.context["og_image_url"]
            == "/media/organizerlist_thumbnail/orgtaro.jpg"
        )
        assert "organizerlist/no_image.png" not in str(response.content)

    def test_メイン画像もサムネイルもNullの時はNoImage画像を表示すること(self, client):

        # arrange
        from factories import OrganizerProfileFactory

        OrganizerProfileFactory(
            code="orgtaro",
            thumbnail_image=None,
            main_image=None,
            og_image=None,
        )

        # act
        response = client.get("/organization/organizers_profile/orgtaro")

        # assert
        assert response.status_code == 200
        assert response.context["image_url"] is None
        assert response.context["og_image_url"] is None
        assert "organizerlist/no_image.png" in str(response.content)

    @pytest.mark.parametrize(
        "visible, expected_status_code",
        [
            (True, 200),
            (False, 404),
        ],
    )
    def test_非表示に設定されている時は404を返すこと(self, client, visible, expected_status_code):

        # arrange
        from factories import OrganizerProfileFactory

        OrganizerProfileFactory(
            code="orgtaro",
            visible=visible,
        )

        # act
        response = client.get("/organization/organizers_profile/orgtaro")

        # assert
        assert response.status_code == expected_status_code

    def test_MarkDownで書かれた自己紹介をHTMLに変換すること(self, client):
        # arrange
        content = """
## あああ
ああああ
## いいい
- 1
- 2
- 3&4
""".strip()

        expected_html = """
<h2>あああ</h2>
<p>ああああ</p>
<h2>いいい</h2>
<ul>
<li>1</li>
<li>2</li>
<li>3&amp;4</li>
</ul>
""".strip()

        from factories import OrganizerProfileFactory

        OrganizerProfileFactory(code="orgtaro", content=content)

        # act
        response = client.get("/organization/organizers_profile/orgtaro")

        # assert
        assert response.status_code == 200
        assert response.context["content"] == expected_html

    def test_MarkDownの中に危険なHTMLがある場合はサニタイズすること(self, client):
        # arrange
        from factories import OrganizerProfileFactory

        OrganizerProfileFactory(code="orgtaro", content="<script>")

        # act
        response = client.get("/organization/organizers_profile/orgtaro")

        # assert
        assert response.status_code == 200
        assert response.context["content"] == "&lt;script&gt;"

    def test_Descriptionが設定されている時はmetaとogpのdescriptionに設定されること(self, client):
        # arrange
        from factories import OrganizerProfileFactory

        OrganizerProfileFactory(
            code="orgtaro", name="オーガナイザー太郎", description="初めましてオーガナイザー太郎でござる"
        )

        # act
        response = client.get("/organization/organizers_profile/orgtaro")
        content = response.content.decode("UTF-8")

        # assert
        assert response.status_code == 200
        assert (
            '<meta name="description" content="メイドカフェでノマド会認定イベントオーガナイザー オーガナイザー太郎 を紹介します。初めましてオーガナイザー太郎でござる" />'
            in content
        )
        assert (
            '<meta property="og:description" content="初めましてオーガナイザー太郎でござる" />' in content
        )

    def test_Descriptionが設定されていない時はmetaとogpのdescriptionに紹介文が設定されること(self, client):
        # arrange
        from factories import OrganizerProfileFactory

        OrganizerProfileFactory(code="orgtaro", name="オーガナイザー太郎", description="")

        # act
        response = client.get("/organization/organizers_profile/orgtaro")
        content = response.content.decode("UTF-8")

        # assert
        assert response.status_code == 200
        assert (
            '<meta name="description" content="メイドカフェでノマド会認定イベントオーガナイザー オーガナイザー太郎 を紹介します。" />'
            in content
        )
        assert (
            '<meta property="og:description" content="メイドカフェでノマド会認定イベントオーガナイザー オーガナイザー太郎 を紹介します。" />'
            in content
        )
