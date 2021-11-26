from django.conf import settings
from django.contrib.sitemaps import Sitemap


class MaidnomadwebSitemap(Sitemap):
    def get_urls(self, page=1, site=None, protocol=None):
        protocol, domain = settings.SITE_ROOT_URL.split("://")
        return self._urls(page, protocol, domain)
