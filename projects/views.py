from django.shortcuts import render, get_object_or_404
from .models import Project


def homepage(request):
    """
    Projects homepage.

    Context variables:
        - `base_template`: The base template to extend from,
           depending on the request type.
    """

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    return render(
        request,
        "projects/index.html",
        {"base_template": base_template},
    )


def project_detail(request, slug):
    """
    Project detail view.

    Parameters:
        - `slug`: The project's unique slug identifier.
    Context variables:
        - `project`: The Project object to be displayed.
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


def project_list(request):
    """
    Project list view.

    Context variables:
        - `projects`: An object containing all published project data.
        - `base_template`: The base template to extend from,
           depending on the request type.
    """

    project_list = Project.objects.filter(status='PB')

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'projects': project_list,
        'base_template': base_template,
    }
    return render(request,
                  'projects/list.html',
                  context)
