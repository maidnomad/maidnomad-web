from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.utils.html import format_html
from reversion.admin import VersionAdmin

from .models import MaidProfile


@admin.register(MaidProfile)
class MaidProfileAdmin(OrderableAdmin, VersionAdmin):
    def thumbnail_image_tag(self, obj):
        return format_html(
            f'<img src="{obj.thumbnail_image.url}" style="height: 120px; width: auto" />'
        )

    thumbnail_image_tag.short_description = "サムネイル画像（プレビュー）"

    def main_image_tag(self, obj):
        return format_html(
            f'<img src="{obj.main_image.url}" style="height: 270px; width: auto" />'
        )

    main_image_tag.short_description = "メイン画像（プレビュー）"

    ordering_field = "order"
    fields = [
        "code",
        "name",
        "content",
        "thumbnail_image",
        "thumbnail_image_tag",
        "main_image",
        "main_image_tag",
        "visible",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "thumbnail_image_tag",
        "main_image_tag",
        "created_at",
        "updated_at",
    ]
    list_display = ("__str__", "order")
    ordering_field_hide_input = "order"
    list_editable = ["order"]
