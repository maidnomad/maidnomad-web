from apps.stafflist.models import StaffProfile


class MaidProfile(StaffProfile):
    thumbnail_image_upload_prefix = "maidlist_thumbnail/"
    main_image_upload_prefix = "maidlist_main/"
    og_image_upload_prefix = "maidlist_ogp/"

    class Meta:
        verbose_name = "メイドさん自己紹介"
        verbose_name_plural = "メイドさん自己紹介"
        ordering = ["order"]
