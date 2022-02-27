from abc import ABCMeta

import bleach
from bleach_allowlist import markdown_tags
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from markdown import markdown

from .models import StaffProfile


class StaffProfileViewSet(metaclass=ABCMeta):
    """汎用スタッフリストビュー生成クラス

    メイドさん紹介など、プロフィールを紹介するページに必要なviewを生成するクラスです。
    使用する時は、このクラスは継承し、属性項目を設定してください。

    属性についてはコードコメントを読んでください。

    インスタンス化して `as_xxx_view` 関数を呼び出すことで、
    urls.py に設定できるビュー関数を返却します。

    ただし直接呼び出すことは必要はありません。
    `urls.get_staff_profile_urlpatterns` 関数
    に渡すことで必要な一連のビューを生成します。

    このクラスは継承して使用するための抽象クラスです。
    直接インスタンス化して使用することを想定していません。
    """

    # ここには StaffProfile のサブクラスを何か必ず設定してください
    model_cls = StaffProfile
    # 以下の設定はほぼ全てする必要があります。
    # ここには画面に表示する名称を記入してください
    verbose_name = "スタッフ紹介"
    return_index_link_text = "スタッフ一覧へ"
    # プロフィールの肩書きを指定してください
    profile_title = "メイドカフェでノマド会スタッフ"
    # 一覧ページのdescriptionに設定する内容を記入してください
    index_description = "スタッフを紹介します"
    # パンくずリストで親になるページ名・表示名を記入してください
    # 運営体制の下に記載する場合はこの項目はそのままで問題ありません
    parent_name = "organization"
    parent_verbose_name = "運営体制"
    # テンプレート・各ページ名を設定してください
    # 基本的にはstafflistの代わりにアプリ名を設定（例:maidlist/index.htmlなど）
    index_template = "stafflist/index.html"
    detail_template = "stafflist/detail.html"
    index_name = "stafflist:index"
    detail_name = "stafflist:detail"

    def _breadcrumbs_to_parent(self):
        """親ページまでのパンくずデータを返します"""
        return [
            {
                "text": "TopPage",
                "url": reverse("top"),
            },
            {
                "text": self.parent_verbose_name,
                "url": reverse(self.parent_name),
            },
        ]

    def as_index_view(self):
        """indexページのview関数を返します"""

        def view_func(request: HttpRequest) -> HttpResponse:
            profiles_list = self._get_profiles_list(request)
            return render(
                request,
                self.index_template,
                {
                    "viewset": self,
                    # カノニカルはブレることがないようにあえて自動解決ではなく指定する
                    "canonical_url": settings.SITE_ROOT_URL + reverse(self.index_name),
                    "breadcrumbs": self._breadcrumbs_to_parent()
                    + [
                        {
                            "text": self.verbose_name,
                        },
                    ],
                    "staff_list": self._to_staff_list(profiles_list),
                },
            )

        return view_func

    def _get_profiles_list(self, request: HttpRequest):
        """プロフィールに必要なリストを検索します"""

        return (
            self.model_cls.objects.only(
                "code",
                "name",
                "main_image",
                "thumbnail_image",
            )
            .filter(
                visible=True,
            )
            .order_by(
                "order",
            )
        )

    def _to_staff_list(self, profiles_list: list[StaffProfile]):
        """スタッフプロフィールリストを画面表示用に整形します"""

        staff_list = []
        for profile in profiles_list:
            staff = {"code": profile.code, "name": profile.name}
            if profile.thumbnail_image:
                staff["image_url"] = profile.thumbnail_image.url
            elif profile.main_image:
                staff["image_url"] = profile.main_image.url
            else:
                staff["image_url"] = None
            staff_list.append(staff)

        return staff_list

    def as_detail_view(self):
        """詳細ページのview関数を返します"""

        def view_func(request: HttpRequest, code: str) -> HttpResponse:
            staff_profile = get_object_or_404(self.model_cls, code=code)

            if not staff_profile.visible:
                raise Http404()

            # カノニカルはブレることがないようにあえて自動解決ではなく指定する
            canonical_url = settings.SITE_ROOT_URL + reverse(
                self.detail_name, kwargs={"code": code}
            )
            return render(
                request,
                self.detail_template,
                {
                    "viewset": self,
                    "canonical_url": canonical_url,
                    "breadcrumbs": self._breadcrumbs_to_parent()
                    + [
                        {
                            # stafflist index ページ
                            "text": self.verbose_name,
                            "url": reverse(self.index_name),
                        },
                        {
                            "text": staff_profile.name,
                        },
                    ],
                    "profile": staff_profile,
                    "image_url": self._to_detail_image_url(staff_profile),
                    "og_image_url": self._to_og_image_url(staff_profile),
                    "content": self._to_content_html_safe(staff_profile.content),
                },
            )

        return view_func

    def _to_content_html_safe(self, content: str) -> str:
        """プロフィールのコンテンツをHTMLに変換します。

        この関数のレスポンスは危険なタグをサニタイズ済みのHTMLであり、
        エスケープせずに出力しても安全です。
        """

        content_html = markdown(content, extensions=["nl2br"])
        # unsafe でレンダリングするのでHTMLをサニタイズする
        content_html_safe = bleach.clean(content_html, markdown_tags)
        return content_html_safe

    def _to_detail_image_url(self, profile: StaffProfile):
        """詳細画像のURLを返します"""

        if profile.main_image:
            return profile.main_image.url
        if profile.thumbnail_image:
            return profile.thumbnail_image.url
        return None

    def _to_og_image_url(self, profile: StaffProfile):
        """ogp画像のURLを返します"""

        if profile.og_image:
            return profile.og_image.url
        if profile.thumbnail_image:
            return profile.thumbnail_image.url
        if profile.main_image:
            return profile.main_image.url
        return None
