import json
import logging
from typing import Any, TypedDict

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


class To(TypedDict):
    slack_user: str

def _post_to_slack(payload):

    """Slack Incoming Webhook API を呼び出す"""
    url = settings.SLACK_WEEBHOOK_URL
    if url:
        data = {"payload": json.dumps(payload)}
        logger.debug("post %s, body %s", url, data)
        requests.post(
            settings.SLACK_WEEBHOOK_URL,
            data=data,
        )

def _notify(message: str, to: To):
    """任意の通知先に情報を通知する"""
    logger.debug("notify %s, to %s", message, to)
    for user in to.get("slack_user", "").split(","):
        user = user.strip()
        if user:
            _post_to_slack(
                {
                    "channel": user,
                    "text": message,
                },
            )
    # 現時点ではslack DMのみ対応しているが必要に応じて、以下に別の通知方法（メールなど）も追加する


def event_schedule_added(to: To, event_name: str, event_url: str, name: str):
    to = To()
    message = (
        f"{name} さんが <{settings.SITE_ROOT_URL + event_url}|{event_name}> の予定を登録したよ。"
    )
    _notify(message, to)


def event_schedule_updated(to: To, event_name: str, event_url: str, name: str):
    message = (
        f"{name} さんが <{settings.SITE_ROOT_URL + event_url}|{event_name}> の予定を更新したよ。"
    )
    _notify(message, to)
