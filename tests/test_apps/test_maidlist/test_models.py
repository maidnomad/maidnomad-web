import pytest


@pytest.mark.django_db
class TestMaidProfile:
    def test_str(self):
        """__str__メソッドが期待通りの値を返すこと"""

        from factories import MaidProfileFactory

        maidchan = MaidProfileFactory(code="maidchan", name="メイドちゃん")

        assert str(maidchan) == "メイドちゃん (maidchan)"
