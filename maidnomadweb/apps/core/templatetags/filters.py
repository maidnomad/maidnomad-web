from django import template

register = template.Library()


@register.filter
def removelines(value):
    """改行文字を取り除きます"""
    return value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ")
