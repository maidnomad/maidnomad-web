import bleach
from bleach_allowlist import markdown_tags
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from markdown import markdown

from .models import StaffProfile


class StaffProfileViewSet:
    verbose_name = "スタッフ紹介"
    return_index_link_text = "スタッフ一覧へ"
    model_cls = StaffProfile
    parent_name = "organization"
    parent_verbose_name = "運営体制"
    index_template = "stafflist/index.html"
    detail_template = "stafflist/detail.html"
    index_name = "stafflist:index"
    detail_name = "stafflist:detail"
    index_description = "スタッフを紹介します"

    def _breadcrumbs_to_parent(self):
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

    def get_profiles_list(self, request: HttpRequest):
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

    def as_index_view(self):
        def view_func(request: HttpRequest) -> HttpResponse:
            profiles_list = self.get_profiles_list(request)
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

    def _to_staff_list(self, profiles_list):
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
        content_html = markdown(content)
        # unsafe でレンダリングするのでHTMLをサニタイズする
        content_html_safe = bleach.clean(content_html, markdown_tags)
        return content_html_safe

    def _to_detail_image_url(self, profile: StaffProfile):
        if profile.main_image:
            return profile.main_image.url
        if profile.thumbnail_image:
            return profile.thumbnail_image.url
        return None

    def _to_og_image_url(self, profile: StaffProfile):
        if profile.og_image:
            return profile.og_image.url
        if profile.thumbnail_image:
            return profile.thumbnail_image.url
        if profile.main_image:
            return profile.main_image.url
        return None
