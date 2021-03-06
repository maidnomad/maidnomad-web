from apps.staticpage import views
from django.shortcuts import redirect
from django.urls import path, reverse

urlpatterns = [
    path("", **views.staticpage("top")),
    path("information/maidnomad_info", **views.staticpage("maidnomad_info")),
    path("information/maidcafe_info", **views.staticpage("maidcafe_info")),
    path("organization", **views.staticpage("organization")),
    # 旧サイトからの301リダイレクト
    path(
        "information/for_maidcafe_info",
        lambda request: redirect(reverse("maidnomad_info"), permanent=True),
    ),
    path(
        "information/akihabara_nomad_maid",
        lambda request: redirect(reverse("maidcafe_info"), permanent=True),
    ),
]
