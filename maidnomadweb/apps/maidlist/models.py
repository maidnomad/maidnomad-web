from django.db.models import ImageField, Model
from django.db.models.fields import (
    BooleanField,
    CharField,
    DateTimeField,
    IntegerField,
    TextField,
)


class MaidProfile(Model):
    code = CharField("英語表記", max_length=50, unique=True)
    name = CharField("名前", max_length=128)
    content = TextField("自己紹介", blank=True)
    thumbnail_image = ImageField(
        "サムネイル画像", upload_to="maidlist_thubnail/", null=True, blank=True
    )
    main_image = ImageField("メイン画像", upload_to="maidlist_main/", null=True, blank=True)

    visible = BooleanField("表示", default=True)
    order = IntegerField("表示順", default=0, db_index=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "メイドさん自己紹介"
        verbose_name_plural = "メイドさん自己紹介"
        ordering = ["order"]
