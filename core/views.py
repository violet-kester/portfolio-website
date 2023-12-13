from blog.models import Post
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import render
from .forms import SearchForm


def homepage(request):
    """
    Homepage.
    """

    return render(request, 'core/index.html')


def search(request):
    """
    Renders a template of blog posts and portfolio projects matching a query.

    Context variables:
        - `query` - The query string entered by the user.
        - `posts` - A QuerySet of Post objects that match the query by title
                      or body, ordered by relevance.
        - `projects` - A QuerySet of Project objects that match the query by title
                      or description, ordered by relevance.
    """

    query = None
    post_results = []
    project_results = []

    if 'query' in request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            # Get cleaned query data from the form
            # The `cleaned_data` dictionary contains the validated form data
            query = form.cleaned_data['query']

            # Get post results
            # Create a search vector based on title and body fields of posts
            search_vector = SearchVector('title', 'body')
            # Use the search vector and query to filter posts by status,
            # annotate posts with a search rank based on relevance,
            # and order posts by descending rank value
            post_results = Post.objects.filter(status='PB').annotate(
                search=search_vector,
                rank=SearchRank(search_vector, query)
            ).filter(search=query).order_by('-rank')

            # TODO:
            # Get project results

    context = {
        'query': query,
        'posts': post_results,
        'projects': project_results,
    }

    return render(request,
                  'core/search.html',
                  context)
