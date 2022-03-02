from pathlib import Path

from django import template

register = template.Library()


@register.simple_tag
def timestamp(path: str):
    """指定したパスのファイルが存在すればタイムスタンプを返します"""
    path = path.replace("..", ".")
    return (Path("maidnomadweb") / path).stat().st_mtime
