from import_export import resources

from .models import MaidProfile


class MaidProfileResource(resources.ModelResource):
    class Meta:
        model = MaidProfile
        import_id_fields = {
            "code",
        }
        skip_unchanged = True

        fields = [
            "code",
            "name",
            "content",
            "thumbnail_image",
            "main_image",
            "visible",
            "order",
        ]
