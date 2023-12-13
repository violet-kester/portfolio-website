from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()


@register.simple_tag
def get_total_posts():
    """Returns the number of published posts."""

    return Post.objects.filter(status='PB').count()


@register.inclusion_tag('blog/post/latest_posts.html')
def get_latest_posts(count=5):
    """Displays the latest published posts."""

    latest_posts = Post.objects.filter(
        status='PB').order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """Returns a list of most commented published posts."""

    return Post.objects.filter(status='PB').annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """Converts a text to HTML using markdown syntax."""

    return mark_safe(markdown.markdown(text))
