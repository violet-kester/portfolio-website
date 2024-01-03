from django import template
from django.utils.safestring import mark_safe
import markdown
import pygments

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    """Converts a text to HTML using markdown syntax."""

    return mark_safe(
        markdown.markdown(text, extensions=['fenced_code', 'codehilite'])
    )
