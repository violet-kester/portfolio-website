from django.contrib import messages
from django.contrib.postgres.search import SearchRank, SearchVector
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import CommentForm, SearchForm, SharePostForm
from .models import Post
from taggit.models import Tag


def homepage(request):
    """
    Blog homepage.

    Context variables:
        - `posts`: A QuerySet of all published Post objects.
        - `base_template`: The base template to extend from,
                           depending on the request type.
    """

    posts = Post.objects.filter(status='PB')

    if request.htmx:
        base_template = '_partial.html'
    else:
        base_template = '_base.html'

    context = {
        'posts': posts,
        'base_template': base_template,
    }
    return render(
        request,
        'blog/index.html',
        context,
    )


def post_detail(request, post_slug):
    """
    Post detail view.

    Renders a template displaying a single published post,
    along with its comments, a form for posting new comments,
    and a list of recommended posts.

    Parameters:
        - `post_slug`: The post's unique slug id.

    Context variables:
       - `post`: The Post object representing the displayed post.
       - `comments`: A QuerySet of active comment objects related to the post.
       - `form`: An instance of the CommentForm for posting new comments.
       - `similar_posts`: A QuerySet of recommended Posts based on shared tags.
       - `base_template`: The base template to extend from,
                          depending on the request type.
    """

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post_slug)
    form = CommentForm()
    comments = post.comments.filter(active=True)
    post_tags = post.tags.all()
    post_tags_ids = post_tags.values_list('id', flat=True)
    # Similar, recommended posts ranked by number of shared tags
    similar_posts = Post.objects.filter(status='PB')\
                                .filter(tags__in=post_tags_ids)\
                                .exclude(id=post.id)
    # Annotate each post with the number of tags shared with the current post
    # Order similar posts by the number of shared tags in descending order
    # Limit results to the first four posts
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]

    if request.htmx:
        base_template = '_partial.html'
    else:
        base_template = '_base.html'

    context = {
        'post': post,
        'post_tags': post_tags,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
        'base_template': base_template,
    }
    return render(request,
                  'blog/post/detail.html',
                  context)


def post_list(request, tag_slug=None):
    """
    Post list view.

    Renders a template of published blog posts, optionally filtered by a tag.

    Parameters:
        - (Optional) `tag_slug`: The slug id of the tag to filter by.

    Context variables:
        - `posts`: A list of Post objects.
        - `tag`: A Tag object if a tag slug is provided, or None.
        - `base_template`: The base template to extend from,
                           depending on the request type.
    """

    posts = Post.objects.filter(status='PB')
    tag = None

    if request.htmx:
        base_template = '_partial.html'
    else:
        base_template = '_base.html'

    # If a tag slug is provided, filter posts by tag
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        context = {
            'posts': posts,
            'tag': tag,
            'base_template': base_template,
        }
        return render(request,
                      'blog/post/tag_results.html',
                      context)

    # Else return all published posts
    context = {
        'posts': posts,
        'tag': tag,
        'base_template': base_template,
    }
    return render(request,
                  'blog/post/list.html',
                  context)


def post_share(request, post_slug):
    """
    Post share view.

    Handles both GET and POST requests for sharing a post by email.
        - GET: Returns the share post form template.
        - POST: Sends an email with a link to the recipient.
          Renders a confirmation message template after the email is sent.

    Parameters:
        - `post_slug`: The slug id of the post being shared.

    Context variables:
        - `post`: The Post object.
        - `form`: An instance of SharePostForm.
        - `sent`: A boolean indicating whether the email has been sent,
                  used to show/hide HTML content.
        - `base_template`: The base template to extend from,
                           depending on the request type.
    """

    post = get_object_or_404(Post, slug=post_slug,
                             status=Post.Status.PUBLISHED)
    sent = False

    # For POST requests, send an email using the form data
    if request.method == 'POST':
        form = SharePostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{data["senders_name"]} recommends you read "{post.title}"'
            message = f'Read "{post.title}" at:\n' \
                      f'{post_url}\n\n' + \
                      f'{data["senders_name"]}\'s comments:\n' \
                      f'{data["message"]}' if data['message'] else '(empty)'
            send_mail(subject,
                      message,
                      'kester.violet.j@gmail.com',
                      [data['recipients_email']])
            sent = True
    # For other requests, return an empty share post form
    else:
        form = SharePostForm()

    if request.htmx:
        base_template = '_partial.html'
    else:
        base_template = '_base.html'

    context = {
        'post': post,
        'form': form,
        'sent': sent,
        'base_template': base_template,
    }
    return render(request,
                  'blog/post/share.html',
                  context)


@require_POST
def post_comment(request, post_slug):
    """
    Post comment view.

    Handles the creation and display of comments on a blog post.
    Returns a rendered HTML commented to be appended to the comment list.

    Parameters:
        - `post_slug`: The slug id of the post being commented on.

    Context variables:
        - `comment`: The new Comment object.
    """

    post = get_object_or_404(Post, slug=post_slug,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)

    if form.is_valid():
        # Create a comment without saving it to the database
        comment = form.save(commit=False)
        # Assign comment to post
        comment.post = post
        # Save the comment to the database
        comment.save()
        # Flash a success message
        messages.success(request, "Your comment has been added.")

    context = {
        'comment': comment,
    }
    return render(request, 'blog/post/comment.html', context)


# TODO:
# Enable prefix matching, for example:
# Searching for 'app' should return posts containing 'apple' and 'application'.
# Currently, search matches whole words only:
# Searching for 'app' returns 0 results. Searching 'apple' returns 1 result.
def post_search(request):
    """
    Post search view.

    Takes a query string from the user and returns a list of blog posts
    that match the query in their title, body, or overview summary.
    Results are ordered by relevance to the query.

    Context variables:
        - `query` - The search query.
        - `results` - Matching Post objects, ordered by relevance.
    """

    query = None
    results = []

    if 'query' in request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body', 'overview')
            results = Post.objects.filter(status='PB').annotate(
                search=search_vector,
                rank=SearchRank(search_vector, query)
            ).filter(search=query).order_by('-rank')

    context = {
        'query': query,
        'results': results,
    }
    return render(request,
                  'blog/post/search_results.html',
                  context)
