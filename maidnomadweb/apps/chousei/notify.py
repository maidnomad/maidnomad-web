import json
import logging
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import TypedDict

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


# API呼び出し中にリクエストをブロッキングしないため別スレッドのExecutorを作成
# なお、あえてスレッド数を1とすることで、エンドポイントにへの呼び出し頻度を緩和する
# 後々API送信先が増えたときは非同期IOを併用するなど改善を検討する
executor = ThreadPoolExecutor(max_workers=1)


class To(TypedDict):
    slack_user: str


def _post_to_slack(payload):  # pragma: nocover
    """Slack Incoming Webhook API を呼び出す"""
    url = settings.SLACK_WEEBHOOK_URL
    if url:
        data = {"payload": json.dumps(payload)}

        def _do():
            try:
                logger.info("post to slack")
                logger.debug("post %s, body %s", url, data)
                # 現在は性能問題がないためblocking requestを使用する
                # 接続が増えて性能問題が生じたらaiohttp化を検討する
                requests.post(
                    settings.SLACK_WEEBHOOK_URL, data=data, timeout=10  # タイムアウトは10秒とする
                )
                # 連続でリクエストしないよう1秒スリープする
                sleep(1)

            except Exception:
                logger.exception("Exception raised while _post_to_slack._do")

        # 接続結果を待つ必要がないので別スレッドで送信する
        executor.submit(_do)


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
    message = (
        f"{name} さんが <{settings.SITE_ROOT_URL + event_url}|{event_name}> の予定を登録したよ。"
    )
    _notify(message, to)


def event_schedule_updated(to: To, event_name: str, event_url: str, name: str):
    message = (
        f"{name} さんが <{settings.SITE_ROOT_URL + event_url}|{event_name}> の予定を更新したよ。"
    )
    _notify(message, to)
