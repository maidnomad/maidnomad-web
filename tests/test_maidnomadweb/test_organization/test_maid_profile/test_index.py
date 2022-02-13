import pytest


@pytest.mark.django_db
class Testメイドさん紹介一覧ページ:
    def test_メイドさんがorder順に表示されること(self, client):
        # arrange
        from factories.maidlist import MaidProfileFactory

        MaidProfileFactory(
            code="maid1", name="メイド1", order=1, thumbnail_image__filename="maidimg1.jpg"
        )
        MaidProfileFactory(
            code="maid2", name="メイド2", order=2, thumbnail_image__filename="maidimg2.jpg"
        )
        MaidProfileFactory(
            code="maid3", name="メイド3", order=3, thumbnail_image__filename="maidimg3.png"
        )

        # act
        response = client.get("/organization/maid_profile/")

        # assert
        assert response.status_code == 200
        assert response.context["staff_list"] == [
            {
                "code": "maid1",
                "name": "メイド1",
                "image_url": "/media/maidlist_thumbnail/maidimg1.jpg",
            },
            {
                "code": "maid2",
                "name": "メイド2",
                "image_url": "/media/maidlist_thumbnail/maidimg2.jpg",
            },
            {
                "code": "maid3",
                "name": "メイド3",
                "image_url": "/media/maidlist_thumbnail/maidimg3.png",
            },
        ]

    def test_非表示のメイドさんは表示されないこと(self, client):
        # arrange
        from factories.maidlist import MaidProfileFactory

        MaidProfileFactory(
            code="maid1",
            name="メイド1",
            order=1,
            thumbnail_image__filename="maidimg1.jpg",
            visible=False,
        )
        MaidProfileFactory(
            code="maid2",
            name="メイド2",
            order=2,
            thumbnail_image__filename="maidimg2.jpg",
        )

        # act
        response = client.get("/organization/maid_profile/")

        # assert
        assert response.status_code == 200
        assert response.context["staff_list"] == [
            {
                "code": "maid2",
                "name": "メイド2",
                "image_url": "/media/maidlist_thumbnail/maidimg2.jpg",
            },
        ]

    def test_サムネイル画像なしの場合メイン画像が表示される(self, client):
        # arrange
        from factories.maidlist import MaidProfileFactory

        MaidProfileFactory(
            code="maidchan",
            name="メイドちゃん",
            thumbnail_image=None,
            main_image__filename="maidchan.jpg",
        )

        # act
        response = client.get("/organization/maid_profile/")

        # assert
        assert response.status_code == 200
        assert response.context["staff_list"] == [
            {
                "code": "maidchan",
                "name": "メイドちゃん",
                "image_url": "/media/maidlist_main/maidchan.jpg",
            }
        ]
        assert "maidlist/no_image.png" not in str(response.content)

    def test_サムネイル画像もメイン画像もない時はnoimage画像が表示されること(self, client):
        # arrange
        from factories.maidlist import MaidProfileFactory

        MaidProfileFactory(
            code="maidchan", name="メイドちゃん", thumbnail_image=None, main_image=None
        )

        # act
        response = client.get("/organization/maid_profile/")

        # assert
        assert response.status_code == 200
        assert response.context["staff_list"] == [
            {
                "code": "maidchan",
                "name": "メイドちゃん",
                "image_url": None,
            }
        ]
        assert "maidlist/no_image.png" in str(response.content)
