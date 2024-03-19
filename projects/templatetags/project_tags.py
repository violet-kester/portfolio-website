from django import template
from ..models import Project

register = template.Library()


@register.inclusion_tag('projects/latest_projects.html')
def get_latest_projects(count=3):
    """
    Retrieves the latest `count` number of published projects.
    """

    latest_projects = Project.objects.filter(
        status='PB'
    ).order_by('-created')[:count]

    return {'latest_projects': latest_projects}


@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiplies the value by the arg.
    Used to modify animation transition times.
    """
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''
