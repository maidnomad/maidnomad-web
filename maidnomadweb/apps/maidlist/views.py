from apps.stafflist.views import StaffProfileViewSet

from .models import MaidProfile


class MaidProfileViewSet(StaffProfileViewSet):
    """メイドさんプロフィールビュー生成クラス"""

    # ここには StaffProfile のサブクラスを何か必ず設定してください
    model_cls = MaidProfile
    # 以下の設定はほぼ全てする必要があります。
    # ここには画面に表示する名称を記入してください
    verbose_name = "メイドさん紹介"
    return_index_link_text = "メイドさん一覧へ"
    # プロフィールの肩書きを指定してください
    profile_title = "メイドカフェでノマド会所属メイド"
    # 一覧ページのdescriptionに設定する内容を記入してください
    index_description = "メイドカフェでノマド会所属のメイドさんを紹介します。"
    # パンくずリストで親になるページ名・表示名を記入してください
    # 運営体制の下に記載する場合はこの項目はそのままで問題ありません
    parent_name = "organization"
    parent_verbose_name = "運営体制"
    # テンプレート・各ページ名を設定してください
    # 基本的にはstafflistの代わりにアプリ名を設定（例:maidlist/index.htmlなど）
    index_template = "maidlist/index.html"
    detail_template = "maidlist/detail.html"
    index_name = "maidlist:index"
    detail_name = "maidlist:detail"
