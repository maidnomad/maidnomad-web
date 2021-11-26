from apps.stafflist.models import StaffProfile


class MaidProfile(StaffProfile):
    class Meta:
        verbose_name = "メイドさん自己紹介"
        verbose_name_plural = "メイドさん自己紹介"
        ordering = ["order"]
