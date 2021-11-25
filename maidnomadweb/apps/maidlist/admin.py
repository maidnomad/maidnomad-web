from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ExportActionMixin, ImportMixin
from import_export.formats import base_formats
from reversion.admin import VersionAdmin

from .models import MaidProfile
from .resources import MaidProfileResource


@admin.register(MaidProfile)
class MaidProfileAdmin(ExportActionMixin, ImportMixin, OrderableAdmin, VersionAdmin):
    def thumbnail_image_tag(self, obj):
        return format_html(
            f'<img src="{obj.thumbnail_image.url}" style="height: 120px; width: auto" />'
        )

    thumbnail_image_tag.short_description = "サムネイル画像（プレビュー）"  # type: ignore

    def main_image_tag(self, obj):
        return format_html(
            f'<img src="{obj.main_image.url}" style="height: 270px; width: auto" />'
        )

    main_image_tag.short_description = "メイン画像（プレビュー）"  # type: ignore

    def og_image_tag(self, obj):
        return format_html(
            f'<img src="{obj.og_image.url}" style="max-height: 120px; width: 120px;" />'
        )

    og_image_tag.short_description = "メイン画像（OGP）"  # type: ignore

    fields = [
        "code",
        "name",
        "content",
        "main_image",
        "main_image_tag",
        "thumbnail_image",
        "thumbnail_image_tag",
        "og_image",
        "og_image_tag",
        "visible",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "main_image_tag",
        "thumbnail_image_tag",
        "og_image_tag",
        "created_at",
        "updated_at",
    ]

    # for ordering
    ordering_field = "order"
    list_display = ("__str__", "order")
    ordering_field_hide_input = "order"
    list_editable = ["order"]

    # for import-export
    resource_class = MaidProfileResource
    formats = [base_formats.CSV, base_formats.JSON]  # yamlも使いたいがバグってるので、今回は無効とする

    # for buttons
    change_list_template = "admin/maidlist/change_list.html"

    # フィルタ
    list_filter = ["visible"]
