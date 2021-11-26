from django.urls import path


def get_staff_profile_urlpatterns(profile_view_set_cls):
    profile_view_set = profile_view_set_cls()
    return [
        path("", profile_view_set.as_index_view(), name="index"),
        path("<str:code>", profile_view_set.as_detail_view(), name="detail"),
    ]
