import logging
import types
from typing import Any, Optional

import pytest
from bs4 import BeautifulSoup, Tag
from django.test import Client

logger = logging.getLogger(__name__)


@pytest.fixture
@pytest.mark.django_db
def superuser(superuser_password):
    from django.contrib.auth.models import User

    user = User.objects.create_superuser(
        "superuser", "superuser@example.com", superuser_password
    )
    return user


@pytest.fixture
def superuser_password():
    return "password"


@pytest.fixture
def form_client(client):
    """get_and_submit, submit_from_soupメソッドを使えるようにしたclient"""

    client.get_and_submit = types.MethodType(get_and_submit, client)
    client.submit_from_soup = types.MethodType(submit_from_soup, client)
    return client


def get_and_submit(
    self: Client,
    path: str,
    data: Optional[dict[str, Any]] = None,
    selector: str = "form",
):
    """ページにアクセス後返却されるフォームを解釈してsubmitします"""
    if data is None:
        data = {}

    response = self.get(path, follow=True)
    soup = BeautifulSoup(response.content, "html.parser")
    return self.submit_from_soup(path, soup, data=data, selector=selector)


def submit_from_soup(
    self: Client,
    path: str,
    soup: BeautifulSoup,
    data: Optional[dict[str, Any]] = None,
    selector: str = "form",
):
    """soupをもとにHTMLを解釈してフォームをsubmitします"""
    if data is None:
        data = {}

    # form tag must <form>
    form = soup.select_one(selector)
    assert form is not None, "レスポンスにformタグが見つかりません"
    assert form.name == "form", "セレクターにマッチする要素がform以外でした"

    action, method, form_data = _get_action_method_data_from_formtag(form, path)
    form_data.update(data)

    print("action:", action)
    print("method: ", method)
    print("data:", form_data)

    if method.lower() == "post":
        return self.post(action, form_data, follow=True)
    if method.lower() == "get":
        return self.get(action, form_data, follow=True)
    raise Exception("unknown mehood: " + method)


def _get_action_method_data_from_formtag(form: Tag, path: str):
    """formタグを解析します

    ブラウザと同じ挙動をするように、action, method, data を取得します

    :param form: formタグを表すTag
    :param path: action属性が省略された時に指定するパス
    :return: action, method, data
    """
    action = form.get("action")
    if not action:
        action = path
        logger.debug("action was not set so submit: %s", path)
    method = form.get("method")
    if not method:
        method = "get"
        logger.debug("method was not set so set get")

    data = {
        input["name"]: input["value"] if input.has_attr("value") else ""
        for input in form.find_all("input")
        if input.has_attr("name") and input.get("type") not in ("checkbox", "submit")
    }

    # チェックボックスの解釈
    for checkbox in form.select("input[type=checkbox]"):
        if checkbox.has_attr("checked"):
            data[checkbox["name"]] = (
                checkbox["value"] if checkbox.has_attr("value") else "on"
            )

    return action, method, data


@pytest.fixture
def client_superuser_loggedin(form_client, superuser, superuser_password):
    """スーパーユーザーでログイン済みのclient"""
    form_client.get_and_submit(
        "/__django_admin/",
        selector="form#login-form",
        data={"username": superuser.username, "password": superuser_password},
    )
    return form_client
