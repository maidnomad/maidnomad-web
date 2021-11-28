import pytest
from bs4 import BeautifulSoup


class TestGetActionMethodDataFromFormtag:
    @pytest.fixture
    def target(self):
        from .conftest import _get_action_method_data_from_formtag

        return _get_action_method_data_from_formtag

    params = {
        "simple_case": (
            """
            <form action="foo" method="post">
                <input type="hidden" name="hhh" value="hhh1" />
                <input type="text" name="ttt" value="ttt1" />
            </form>
            """,
            (
                "foo",
                "post",
                {
                    "hhh": "hhh1",
                    "ttt": "ttt1",
                },
            ),
        ),
        "reading_checkbox": (
            """
            <form action="cfoo" method="get">
                <input type="checkbox" name="c1" checked />
                <input type="checkbox" name="c2" value="c2on" checked />
                <input type="checkbox" name="c3" value="c3on" />
            </form>
            """,
            (
                "cfoo",
                "get",
                {
                    "c1": "on",
                    "c2": "c2on",
                },
            ),
        ),
        "action, method were empty": (
            """
            <form></form>
            """,
            ("/current_page", "get", {}),
        ),
    }

    @pytest.mark.parametrize(
        "formsource, expected", list(params.values()), ids=list(params.keys())
    )
    def test_it(self, target, formsource, expected):
        soup = BeautifulSoup(formsource, "html.parser").find("form")
        actual = target(soup, "/current_page")
        assert actual == expected
