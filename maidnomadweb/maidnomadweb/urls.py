from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

urlpatterns = [
    path("__django_admin/", admin.site.urls),
    path("mdeditor/", include("mdeditor.urls")),
    path(
        "parts/menu_only",
        lambda request: render(request, "menu.html"),
    ),
    path("organization/maid_profile/", include(("apps.maidlist.urls", "maidlist"))),
    path(
        "organization/organizers_profile/",
        include(("apps.organizerlist.urls", "organizerlist")),
    ),
    path("", include("apps.staticpage.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
