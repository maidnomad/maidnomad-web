from datetime import datetime

import pytz

TOKYO_TZ = pytz.timezone("Asia/Tokyo")


def tokyo_datetime(*args, **kwargs):
    return TOKYO_TZ.localize(datetime(*args, **kwargs))
