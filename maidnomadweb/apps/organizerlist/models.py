from apps.stafflist.models import StaffProfile


class OrganizerProfile(StaffProfile):
    thumbnail_image_upload_prefix = "organizerlist_thumbnail/"
    main_image_upload_prefix = "organizerlist_main/"
    og_image_upload_prefix = "organizerlist_ogp/"

    class Meta:
        verbose_name = "イベントオーガナイザー自己紹介"
        verbose_name_plural = "イベントオーガナイザー自己紹介"
        ordering = ["order"]
