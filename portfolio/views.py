from .models import Project
from django.shortcuts import render, get_object_or_404


def homepage(request):
    """
    Portfolio homepage.
    """

    return render(request, 'portfolio/homepage.html')


def project_list(request):
    """
    Project list view.

    Context variables:
       - `projects`: An object containing all published project data.
    """

    project_list = Project.objects.filter(status='PB')
    context = {
        'projects': project_list,
    }

    return render(request, 'portfolio/project/list.html', context)


def project_detail(request, slug):
    """
    Project detail view.

    Parameters:
        - `slug`: The project's unique slug identifier.
    Context variables:
       - `project`: The Project object to be displayed.
    """

    project = get_object_or_404(Project,
                                status=Project.Status.PUBLISHED,
                                slug=slug)
    context = {
        'project': project,
    }

    return render(request, 'portfolio/project/detail.html', context)
