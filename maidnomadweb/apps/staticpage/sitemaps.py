from datetime import datetime
from pathlib import Path

from django.shortcuts import resolve_url
from apps.core.sitemaps import MaidnomadwebSitemap

from .consts import STATICPAGES

class StaticpageSitemap(MaidnomadwebSitemap):
    def items(self):
        return list(STATICPAGES.items())

    def location(self, item):
        key, _ = item
        return resolve_url(key)

    def lastmod(self, item):
        _, staticpage = item
        template_path = Path(__file__).parent / "templates" / staticpage["template"]
        return datetime.fromtimestamp(template_path.stat().st_mtime)
    
    def priority(self, item):
        _, staticpage = item
        return staticpage.get("priority", 0.9)
    
    def changefreq(self, item):
        _, staticpage = item
        return staticpage.get("changefreq", "monthly")
