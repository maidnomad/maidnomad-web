from apps.stafflist.sitemaps import StafflistSitemap

from .models import MaidProfile


class MaidlistSitemap(StafflistSitemap):
    model_cls = MaidProfile
    detail_name = "maidlist:detail"
