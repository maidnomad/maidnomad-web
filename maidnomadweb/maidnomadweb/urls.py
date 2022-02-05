from apps.maidlist.sitemaps import MaidlistSitemap
from apps.organizerlist.sitemaps import OrganizerlistSitemap
from apps.staticpage.sitemaps import StaticpageSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import render
from django.urls import include, path

from .sitemaps import joined_sitemap_index

sitemaps = {
    "staticpage": StaticpageSitemap,
    "maidlist": MaidlistSitemap,
    "organizerlist": OrganizerlistSitemap,
}

urlpatterns = [
    path("__django_admin/", admin.site.urls),
    path("mdeditor/", include("mdeditor.urls")),
    # サイトマップ
    path(
        # "sitemap-.*" を WordPressに割り当てているので、 `_` にしていることに注意
        "sitemap_django.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
    # WordPressとドッキングしたサイトマップ
    path("sitemap.xml", joined_sitemap_index),
    path(
        "parts/menu_only",
        lambda request: render(request, "menu.html"),
    ),
    # 調整
    path("chousei/", include(("apps.chousei.urls", "chousei"))),
    # プロフィールページ
    path("organization/maid_profile/", include(("apps.maidlist.urls", "maidlist"))),
    path(
        "organization/organizers_profile/",
        include(("apps.organizerlist.urls", "organizerlist")),
    ),
    # 静的ページ
    path("", include("apps.staticpage.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
