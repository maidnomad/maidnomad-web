from import_export import resources

from .models import StaffProfile


class StaffProfileResource(resources.ModelResource):
    """自己紹介のインポート・エクスポート機能で使用する項目"""

    class Meta:
        model = StaffProfile
        import_id_fields = {
            "code",
        }
        skip_unchanged = True

        fields = [
            "code",
            "name",
            "description",
            "content",
            "thumbnail_image",
            "main_image",
            "visible",
            "order",
        ]
