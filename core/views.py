from django.shortcuts import render


def homepage(request):
    """
    Homepage.

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
        "core/index.html",
        {"base_template": base_template},
    )


def resume(request):
    """
    View for the resume page.

    Context variables:
        - `base_template`: The base template to extend from,
           depending on the request type.
    """

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'base_template': base_template,
    }
    return render(request,
                  'core/resume.html',
                  context)


def about(request):
    """
    View for the about page.

    Context variables:
        - `base_template`: The base template to extend from,
           depending on the request type.
    """

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'base_template': base_template,
    }
    return render(request,
                  'core/about.html',
                  context)
