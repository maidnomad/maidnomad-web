from django.db.models import ImageField, Model
from django.db.models.fields import (
    BooleanField,
    CharField,
    DateTimeField,
    IntegerField,
    TextField,
)
from mdeditor.fields import MDTextField


class StaffProfile(Model):
    """stafflistの派生アプリでプロフィールとして表示できるベースのモデルです。

    このクラスは抽象クラスであり、必ず継承して使うことを想定しています。
    直接インスタンス化できません。

    必要に応じて項目を足すことはできますが消すことはできません。

    サブクラスではメタクラスを作成し `ordering = ["order"]` を必ず指定してください。
    そうしないと順番の入れ替えが機能しません。
    """

    code = CharField("英語表記", max_length=50, unique=True)
    name = CharField("名前", max_length=128)
    description = TextField("Description", blank=True)
    content = MDTextField("自己紹介", blank=True)
    thumbnail_image = ImageField(
        "サムネイル画像", upload_to="maidlist_thumbnail/", null=True, blank=True
    )
    main_image = ImageField("メイン画像", upload_to="maidlist_main/", null=True, blank=True)
    og_image = ImageField("OGP画像", upload_to="maidlist_ogp/", null=True, blank=True)

    visible = BooleanField("表示", default=True)
    order = IntegerField("表示順", default=0, db_index=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        abstract = True
        ordering = ["order"]
