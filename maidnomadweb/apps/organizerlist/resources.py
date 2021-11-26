from apps.stafflist.resources import StaffProfileResource

from .models import OrganizerProfile


class OrganizerProfileResource(StaffProfileResource):
    """イベントオーガナイザー自己紹介のインポート・エクスポート機能で使用する項目"""

    class Meta:
        model = OrganizerProfile
