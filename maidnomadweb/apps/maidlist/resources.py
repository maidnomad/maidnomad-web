from apps.stafflist.resources import StaffProfileResource

from .models import MaidProfile


class MaidProfileResource(StaffProfileResource):
    """メイドさん自己紹介のインポート・エクスポート機能で使用する項目"""

    class Meta:
        model = MaidProfile
