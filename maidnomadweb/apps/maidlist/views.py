from apps.stafflist.views import StaffProfileViewSet

from .models import MaidProfile


class MaidProfileViewSet(StaffProfileViewSet):
    verbose_name = "メイドさん紹介"
    return_index_link_text = "メイドさん一覧へ"
    profile_title = "メイドカフェでノマド会所属メイド"
    model_cls = MaidProfile
    parent_name = "organization"
    parent_verbose_name = "運営体制"
    index_template = "maidlist/index.html"
    detail_template = "maidlist/detail.html"
    index_name = "maidlist:index"
    detail_name = "maidlist:detail"
    index_description = "メイドカフェでノマド会所属のメイドさんを紹介します。"
