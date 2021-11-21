from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .consts import STATICPAGES


def staticpage(name: str):
    """静的ページを表示するビュー関数を返します。

    urls.py に以下のように指定することを想定しています。
    ```
    path("foo/bar/", *+views.staticpage("foo_bar_page")),
    ```

    :param name: STATICPAGES のキーの中から指定できます
    """

    def inner(request: HttpRequest) -> HttpResponse:
        staticpage = STATICPAGES[name]

        breadcrumbs = None
        if "parent" in staticpage:
            breadcrumbs = _breadcrumbs(name)
            del breadcrumbs[-1]["url"]

        title = None
        if name != "top":
            # top page のみ title はサイトルートそのもの
            title = staticpage.get("title") or staticpage.get("name")

        # top page でも ogp の title は付与する
        ogp_title = staticpage.get("ogp_title") or title
        return render(
            request,
            staticpage["template"],
            {
                "title": title,
                "ogp_title": ogp_title,
                "canonical_url": settings.SITE_ROOT_URL + reverse(name),
                "breadcrumbs": breadcrumbs,
                "ogp_type": staticpage.get("ogp_type"),
                "description": staticpage.get("description"),
            },
        )

    return {"view": inner, "name": name}


def _breadcrumbs(name: str, result: list[dict[str, str]] = []):
    """パンくずリスト用のデータを生成します

    :param name: STATICPAGES のキーの中から指定できます
    :param result: 生成途中のパンくずデータ（再帰呼び出し用）
    :return: コンテキスト変数 breadcrumbs に指定する値
    """
    staticpage = STATICPAGES[name]
    elem = {
        "text": staticpage["title"],
        "url": reverse(name),
    }

    result = [elem] + result
    if "parent" in staticpage:
        parent = staticpage["parent"]
        return _breadcrumbs(parent, result)

    return result
