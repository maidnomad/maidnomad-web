import pytest
from helper import tokyo_datetime


@pytest.mark.django_db
class TestMaidProfile:
    def test_str(self):
        """__str__メソッドが期待通りの値を返すこと"""

        from factories.chousei import EventDateFactory

        event_date = EventDateFactory(start_datetime=tokyo_datetime(2022, 1, 2, 10, 15))

        assert str(event_date) == "2022/01/02(日) 10:15"
