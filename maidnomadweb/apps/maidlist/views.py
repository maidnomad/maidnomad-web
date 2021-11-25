import bleach
from bleach_allowlist import markdown_tags
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from markdown import markdown

from .models import MaidProfile


def index(request: HttpRequest) -> HttpResponse:
    maid_profiles_list = (
        MaidProfile.objects.only(
            "code",
            "name",
            "main_image",
            "thumbnail_image",
            "og_image",
        )
        .filter(
            visible=True,
        )
        .order_by(
            "order",
        )
    )
    return render(
        request,
        "maidlist/index.html",
        {
            "canonical_url": settings.SITE_ROOT_URL + reverse("maidlist:index"),
            "breadcrumbs": [
                {
                    "text": "TopPage",
                    "url": reverse("top"),
                },
                {
                    "text": "運営体制",
                    "url": reverse("organization"),
                },
                {
                    "text": "メイドさん紹介",
                },
            ],
            "maid_list": _to_maid_list(maid_profiles_list),
        },
    )


def _to_maid_list(maid_profiles_list):
    maid_list = []
    for maid_profile in maid_profiles_list:
        maid = {"code": maid_profile.code}
        if maid_profile.thumbnail_image:
            maid["image_url"] = maid_profile.thumbnail_image.url
        elif maid_profile.main_image:
            maid["image_url"] = maid_profile.main_image.url
        else:
            maid["image_url"] = None
        maid_list.append(maid)
    return maid_list


def detail(request: HttpRequest, code: str) -> HttpResponse:
    maid_profile = get_object_or_404(MaidProfile, code=code)

    if not maid_profile.visible:
        raise Http404()

    canonical_url = settings.SITE_ROOT_URL + reverse(
        "maidlist:detail", kwargs={"code": code}
    )
    return render(
        request,
        "maidlist/detail.html",
        {
            "canonical_url": canonical_url,
            "breadcrumbs": [
                {
                    "text": "TopPage",
                    "url": reverse("top"),
                },
                {
                    "text": "運営体制",
                    "url": reverse("organization"),
                },
                {
                    "text": "メイドさん紹介",
                    "url": reverse("maidlist:index"),
                },
                {
                    "text": maid_profile.name,
                },
            ],
            "maid_profile": maid_profile,
            "image_url": _to_detail_image_url(maid_profile),
            "og_image_url": _to_og_image_url(maid_profile),
            "content": _to_content_html_safe(maid_profile.content),
        },
    )


def _to_content_html_safe(content: str) -> str:
    content_html = markdown(content)
    # unsafe でレンダリングするのでHTMLをサニタイズする
    content_html_safe = bleach.clean(content_html, markdown_tags)
    return content_html_safe


def _to_detail_image_url(maid_profile: MaidProfile):
    if maid_profile.main_image:
        return maid_profile.main_image.url
    if maid_profile.thumbnail_image:
        return maid_profile.thumbnail_image.url
    return None


def _to_og_image_url(maid_profile: MaidProfile):
    if maid_profile.og_image:
        return maid_profile.og_image.url
    if maid_profile.thumbnail_image:
        return maid_profile.thumbnail_image.url
    if maid_profile.main_image:
        return maid_profile.main_image.url
    return None
