import pytest


@pytest.mark.django_db
class Testオーガナイザー紹介一覧ページ:
    def test_オーガナイザーがorder順に表示されること(self, client):
        # arrange
        from factories.organizerlist import OrganizerProfileFactory

        OrganizerProfileFactory(
            code="org1",
            name="オーガナイザー1",
            order=1,
            thumbnail_image__filename="orgimg1.jpg",
        )
        OrganizerProfileFactory(
            code="org2",
            name="オーガナイザー2",
            order=2,
            thumbnail_image__filename="orgimg2.jpg",
        )
        OrganizerProfileFactory(
            code="org3",
            name="オーガナイザー3",
            order=3,
            thumbnail_image__filename="orgimg3.png",
        )

        # act
        response = client.get("/organization/organizers_profile/")

        # assert
        assert response.status_code == 200
        assert response.context["staff_list"] == [
            {
                "code": "org1",
                "name": "オーガナイザー1",
                "image_url": "/media/organizerlist_thumbnail/orgimg1.jpg",
            },
            {
                "code": "org2",
                "name": "オーガナイザー2",
                "image_url": "/media/organizerlist_thumbnail/orgimg2.jpg",
            },
            {
                "code": "org3",
                "name": "オーガナイザー3",
                "image_url": "/media/organizerlist_thumbnail/orgimg3.png",
            },
        ]

    def test_非表示のオーガナイザーは表示されないこと(self, client):
        # arrange
        from factories.organizerlist import OrganizerProfileFactory

        OrganizerProfileFactory(
            code="org1",
            name="オーガナイザー1",
            order=1,
            thumbnail_image__filename="orgimg1.jpg",
            visible=False,
        )
        OrganizerProfileFactory(
            code="org2",
            name="オーガナイザー2",
            order=2,
            thumbnail_image__filename="orgimg2.jpg",
        )

        # act
        response = client.get("/organization/organizers_profile/")

        # assert
        assert response.status_code == 200
        assert response.context["staff_list"] == [
            {
                "code": "org2",
                "name": "オーガナイザー2",
                "image_url": "/media/organizerlist_thumbnail/orgimg2.jpg",
            },
        ]

    def test_サムネイル画像なしの場合メイン画像が表示される(self, client):
        # arrange
        from factories.organizerlist import OrganizerProfileFactory

        OrganizerProfileFactory(
            code="orgtaro",
            name="オーガナイザー太郎",
            thumbnail_image=None,
            main_image__filename="orgtaro.jpg",
        )

        # act
        response = client.get("/organization/organizers_profile/")

        # assert
        assert response.status_code == 200
        assert response.context["staff_list"] == [
            {
                "code": "orgtaro",
                "name": "オーガナイザー太郎",
                "image_url": "/media/organizerlist_main/orgtaro.jpg",
            }
        ]
        assert "organizerlist/no_image.png" not in str(response.content)

    def test_サムネイル画像もメイン画像もない時はnoimage画像が表示されること(self, client):
        # arrange
        from factories.organizerlist import OrganizerProfileFactory

        OrganizerProfileFactory(
            code="orgtaro", name="オーガナイザー太郎", thumbnail_image=None, main_image=None
        )

        # act
        response = client.get("/organization/organizers_profile/")

        # assert
        assert response.status_code == 200
        assert response.context["staff_list"] == [
            {
                "code": "orgtaro",
                "name": "オーガナイザー太郎",
                "image_url": None,
            }
        ]
        assert "organizerlist/no_image.png" in str(response.content)
