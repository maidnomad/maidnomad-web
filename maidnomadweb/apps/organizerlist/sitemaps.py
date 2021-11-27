from apps.stafflist.sitemaps import StafflistSitemap

from .models import OrganizerProfile


class OrganizerlistSitemap(StafflistSitemap):
    model_cls = OrganizerProfile
    detail_name = "organizerlist:detail"
