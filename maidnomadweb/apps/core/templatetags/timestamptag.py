from pathlib import Path

from django import template

register = template.Library()


@register.simple_tag
def timestamp(path: str):
    """指定したパスのファイルが存在すればタイムスタンプを返します"""
    path = path.replace("..", ".")
    return (Path(__file__).parent.parent.parent / path).stat().st_mtime
