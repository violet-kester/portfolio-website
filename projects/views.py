from django.shortcuts import render, get_object_or_404
from .models import Project


def homepage(request):
    """
    Projects homepage.

    Context variables:
        - `projects`: A QuerySet of all published Project objects.
        - `base_template`: The base template to extend from,
                           depending on the request type.
    """

    projects = Project.objects.filter(status='PB')

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'projects': projects,
        'base_template': base_template,
    }
    return render(
        request,
        "projects/index.html",
        context,
    )


def project_detail(request, slug):
    """
    Project detail view.

    Parameters:
        - `slug`: The project's unique slug identifier.
    Context variables:
        - `project`: The Project object.
        - `base_template`: The base template to extend from,
                           depending on the request type.
    """

    project = get_object_or_404(Project,
                                status=Project.Status.PUBLISHED,
                                slug=slug)

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'project': project,
        'base_template': base_template,
    }
    return render(request,
                  'projects/detail.html',
                  context)
