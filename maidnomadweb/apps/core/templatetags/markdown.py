from textwrap import dedent

import bleach
from bleach_allowlist import markdown_tags
from django import template
from markdown import markdown

register = template.Library()


@register.tag(name="markdown")
def do_markdown(parser, token):
    nodelist = parser.parse(("endmarkdown",))
    parser.delete_first_token()
    return MarkdownNode(nodelist)


class MarkdownNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        content = dedent(content)
        content_html = markdown(content)
        return content_html
