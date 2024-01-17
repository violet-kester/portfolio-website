from django import template
from ..models import Project

register = template.Library()


@register.inclusion_tag('projects/latest_projects.html')
def get_latest_projects(count=3):
    """Displays the latest published projects."""

    latest_projects = Project.objects.filter(
        status='PB'
    ).order_by('-publish')[:count]

    return {'latest_projects': latest_projects }
