from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("__django_admin/", admin.site.urls),
    path("organization/maid_profile_tmp/", include("apps.maidlist.urls")),
    path("organization/maid_profile/", include("apps.maidlist.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
