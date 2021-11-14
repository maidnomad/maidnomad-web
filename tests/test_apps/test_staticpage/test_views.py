import pytest


class TestBreadCrumbs:
    @pytest.fixture
    def target(self):
        from apps.staticpage.views import _breadcrumbs

        return _breadcrumbs

    @pytest.mark.parametrize(
        "name, expected",
        [
            (
                "top",
                [
                    {
                        "text": "TopPage",
                        "url": "/",
                    },
                ],
            ),
            (
                "maidnomad_info",
                [
                    {
                        "text": "TopPage",
                        "url": "/",
                    },
                    {
                        "text": "メイドカフェ店舗様向けノマド会のご紹介",
                        "url": "/information/maidnomad_info",
                    },
                ],
            ),
            (
                "maidcafe_info",
                [
                    {
                        "text": "TopPage",
                        "url": "/",
                    },
                    {
                        "text": "ノマドができるメイドカフェ紹介",
                        "url": "/information/maidcafe_info",
                    },
                ],
            ),
            (
                "organization",
                [
                    {
                        "text": "TopPage",
                        "url": "/",
                    },
                    {
                        "text": "運営体制",
                        "url": "/organization",
                    },
                ],
            ),
        ],
    )
    def test_it(self, target, name, expected):
        # act
        actual = target(name)
        # assert
        assert actual == expected
