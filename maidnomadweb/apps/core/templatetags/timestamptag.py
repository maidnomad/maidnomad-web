from pathlib import Path

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def timestamp(path: str):
    """指定したパスのファイルが存在すればタイムスタンプを返します"""
    path = path.replace("/../", "/")  # ".." を指定して攻撃を禁止
    return (Path(settings.BASE_DIR) / path).stat().st_mtime
