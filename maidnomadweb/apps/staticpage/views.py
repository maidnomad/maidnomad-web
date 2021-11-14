from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

STATICPAGES = {
    "top": {
        "template": "staticpage/toppage.html",
        "title": "TopPage",
        "ogp_type": "website",
    },
    "maidnomad_info": {
        "template": "staticpage/maidnomad_info.html",
        "title": "メイドカフェ店舗様向けノマド会のご紹介",
        "parent": "top",
    },
    "maidcafe_info": {
        "template": "staticpage/maidcafe_info.html",
        "title": "ノマドができるメイドカフェ紹介",
        "parent": "top",
    },
    "organization": {
        "template": "staticpage/organization.html",
        "title": "運営体制",
        "parent": "top",
    },
}


def staticpage(name: str):
    def inner(request: HttpRequest) -> HttpResponse:
        staticpage = STATICPAGES[name]
        if "parent" in staticpage:
            breadcrumbs = _breadcrumbs(name)
            del breadcrumbs[-1]["url"]
        else:
            breadcrumbs = None
        return render(
            request,
            staticpage["template"],
            {
                "canonical_url": settings.SITE_ROOT_URL + reverse(name),
                "breadcrumbs": breadcrumbs,
                "ogp_type": staticpage.get("ogp_type"),
            },
        )

    return inner


def _breadcrumbs(name: str, result: list[dict[str, str]] = []):
    staticpage = STATICPAGES[name]
    elem = {"text": staticpage["title"], "url": reverse(name)}

    result = [elem] + result
    if "parent" in staticpage:
        parent = staticpage["parent"]
        return _breadcrumbs(parent, result)

    return result
