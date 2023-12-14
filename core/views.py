from blog.models import Post
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import render
from .forms import SearchForm


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