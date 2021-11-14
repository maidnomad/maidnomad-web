from django.conf import settings
from django.http import HttpRequest


def site_common_variables(request: HttpRequest):
    return {
        "SITE_ROOT_URL": settings.SITE_ROOT_URL,
        "SITE_ROOT_TITLE": settings.SITE_ROOT_TITLE,
        "SITE_ROOT_DESCRIPTION": settings.SITE_ROOT_DESCRIPTION,
        "SITE_ADSENSE_TRACKING_ID": settings.SITE_ADSENSE_TRACKING_ID,
        "SITE_ADSENSE_CLIENT": settings.SITE_ADSENSE_CLIENT,
        "SITE_ADSENSE_SLOT_BOX": settings.SITE_ADSENSE_SLOT_BOX,
        "SITE_ADSENSE_SLOT_SIDE": settings.SITE_ADSENSE_SLOT_SIDE,
        "SITE_AMAZON_ASSOCIATE_TRACKING_ID": settings.SITE_AMAZON_ASSOCIATE_TRACKING_ID,
    }
