import pytest


@pytest.mark.django_db
class Testメイドさん紹介詳細ページ:
    def test_メイドさんの名前と画像が表示されること(self, client):
        # arrange
        from factories import MaidProfileFactory

        MaidProfileFactory(
            code="maidchan",
            name="メイドちゃん",
            main_image__filename="maidchan.jpg",
        )

        # act
        response = client.get("/organization/maid_profile/maidchan")

        # assert
        assert response.status_code == 200
        assert response.context["maid_profile"].code == "maidchan"
        assert response.context["maid_profile"].name == "メイドちゃん"
        assert response.context["image_url"] == "/media/maidlist_main/maidchan.jpg"

    def test_メイン画像がNullの時はサムネイル画像を表示すること(self, client):
        # arrange
        from factories import MaidProfileFactory

        MaidProfileFactory(
            code="maidchan",
            thumbnail_image__filename="maidchan.jpg",
            main_image=None,
        )

        # act
        response = client.get("/organization/maid_profile/maidchan")

        # assert
        assert response.status_code == 200
        assert response.context["image_url"] == "/media/maidlist_thumbnail/maidchan.jpg"
        assert "no_image.png" not in str(response.content)

    def test_メイン画像もサムネイルもNullの時はNoImage画像を表示すること(self, client):

        # arrange
        from factories import MaidProfileFactory

        MaidProfileFactory(
            code="maidchan",
            thumbnail_image=None,
            main_image=None,
        )

        # act
        response = client.get("/organization/maid_profile/maidchan")

        # assert
        assert response.status_code == 200
        assert response.context["image_url"] is None
        assert "no_image.png" in str(response.content)

    @pytest.mark.parametrize(
        "visible, expected_status_code",
        [
            (True, 200),
            (False, 404),
        ],
    )
    def test_非表示に設定されている時は404を返すこと(self, client, visible, expected_status_code):

        # arrange
        from factories import MaidProfileFactory

        MaidProfileFactory(
            code="maidchan",
            visible=visible,
        )

        # act
        response = client.get("/organization/maid_profile/maidchan")

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

        from factories import MaidProfileFactory

        MaidProfileFactory(code="maidchan", content=content)

        # act
        response = client.get("/organization/maid_profile/maidchan")

        # assert
        assert response.status_code == 200
        assert response.context["content"] == expected_html

    def test_MarkDownの中に危険なHTMLがある場合はサニタイズすること(self, client):
        # arrange
        from factories import MaidProfileFactory

        MaidProfileFactory(code="maidchan", content="<script>")

        # act
        response = client.get("/organization/maid_profile/maidchan")

        # assert
        assert response.status_code == 200
        assert response.context["content"] == "&lt;script&gt;"