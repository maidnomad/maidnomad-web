from unittest import mock

import pytest


@pytest.fixture(autouse=True)
def mock_post_to_slack():
    # Slack API呼び出しをモック化
    with mock.patch("apps.chousei.notify._post_to_slack") as m:
        yield m
