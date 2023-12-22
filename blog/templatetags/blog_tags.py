from django import template
from django.db.models import Count
from django.db.models.functions import Lower
from ..models import Post
from taggit.models import Tag

register = template.Library()


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


@register.simple_tag
def get_all_post_tags():
    """Returns a list all post tags."""

    return Tag.objects.all().order_by(Lower('name'))


@register.simple_tag
def get_total_posts():
    """Returns the number of published posts."""

    return Post.objects.filter(status='PB').count()
