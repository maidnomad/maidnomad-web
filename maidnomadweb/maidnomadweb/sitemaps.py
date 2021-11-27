# このモジュールは WordPress と Django が共存している間のみ必要な措置
# WordPressのサイトマップはWordPressに生成させたいので、Django側のサイトマップと
# XMLレベルでドッキングしてレスポンスを返す
# WordPressを廃止したらこのモジュールは捨てる

from xml.etree import ElementTree

import requests
from django.conf import settings
from django.http import HttpResponse

NS_SITEMAP = "http://www.sitemaps.org/schemas/sitemap/0.9"


def joined_sitemap_index(request):
    """WordPressのブログのサイトマップと合体したサイトマップインデックスを返す

    WordPressのサイトマップをXMLパースし、このサイトのサイトマップを挿入したサイトマップインデックスを生成する
    """
    response = requests.get(settings.BLOG_SITEMAP_URL)

    django_sitemap = ElementTree.Element(f"{{{NS_SITEMAP}}}sitemap")
    django_sitemap_loc = ElementTree.SubElement(django_sitemap, f"{{{NS_SITEMAP}}}loc")
    django_sitemap_loc.text = settings.SITE_ROOT_URL + "/sitemap_django.xml"

    root = ElementTree.fromstring(response.text)
    root.insert(0, django_sitemap)
    return HttpResponse(
        ElementTree.tostring(root, default_namespace=NS_SITEMAP), "text/xml"
    )
