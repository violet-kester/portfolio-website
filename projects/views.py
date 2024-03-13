from django.shortcuts import render, get_object_or_404
from .models import Project, Technology


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
        - `tech_data`: A dictionary of technologies used to create
                       this project, organized by category.
        - `base_template`: The base template to extend from,
                           depending on the request type.
    """

    project = get_object_or_404(Project,
                                status=Project.Status.PUBLISHED,
                                slug=slug)

    # Populates a dictionary with technology categories as keys
    # and the corresponding technologies as values.
    tech_data = {}
    for category, category_name in Technology.CATEGORY_CHOICES:
        tech_data[category_name] = project.technologies.filter(
            category=category)

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'project': project,
        'tech_data': tech_data,
        'base_template': base_template,
    }
    return render(request,
                  'projects/detail.html',
                  context)
