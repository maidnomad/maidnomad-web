from apps.core.sitemaps import MaidnomadwebSitemap
from django.shortcuts import resolve_url

from .models import StaffProfile


class StafflistSitemap(MaidnomadwebSitemap):
    model_cls = StaffProfile
    detail_name = "stafflist:detail"
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return self.model_cls.objects.only(
            "code",
            "updated_at",
        ).filter(visible=True)

    def location(self, obj):
        return resolve_url(self.detail_name, code=obj.code)

    def lastmod(self, obj):
        return obj.updated_at
