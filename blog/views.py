from django.contrib import messages
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm, SearchForm, SharePostForm
from .models import Post
from taggit.models import Tag


def homepage(request):
    """
    Blog homepage.

    Context variables:
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
    along with comments, a form for posting new comments,
    and a list of recommended posts.

    Parameters:
        - `post_slug`: The post's unique slug identifier.

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
        - (Optional) `tag_slug`: The slug identifier of the tag to filter by.

    Context variables:
        - `posts`: A list of Post objects.
        - `tag`: A Tag object if a tag slug is provided, or None.
        - `base_template`: The base template to extend from,
           depending on the request type.
    """

    posts = Post.objects.filter(status='PB')
    tag = None

    # If a tag slug is provided, filter posts by tag
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    if request.htmx:
        base_template = '_partial.html'
    else:
        base_template = '_base.html'

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
    For GET requests, returns the share post form template.
    For POST requests, sends an email with the post link to the recipient.
    Renders a template with the post, form, and email status.

    Parameters:
        - `post_slug` - The slug identifier of the post being shared.

    Context variables:
        - `post`: The Post object.
        - `form`: An instance of SharePostForm.
        - `sent`: A boolean indicating whether the email has been sent,
           used to show/hide HTML content.
        - `base_template`: The base template to extend from,
           depending on the request type.
    """

    post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = SharePostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{data["senders_name"]} recommends you read "{post.title}"'
            message = f'Read "{post.title}" at:\n' \
                      f'{post_url}\n\n' + \
                      (f'{data["senders_name"]}\'s comments:\n {data["message"]}' if data['message'] else '')
            send_mail(subject,
                      message,
                      'kester.violet.j@gmail.com',
                      [data['recipients_email']])
            sent = True
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


def post_comment (request, post_slug):
    """
    Post comment view.

    Handles both GET and POST requests for commenting on a post.
    For GET requests, returns the comment form template.
    For POST requests, creates a comment and appended it to the comments list.

    Parameters:
        - `post_slug`: The slug identifier of the post being commented on.

    Context variables:
        - `comment`: The new Comment object (only for POST requests).
        - `form`: An instance of the CommentForm.
    """

    post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)
    comment = None

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            # Create a comment without saving it to the database
            comment = form.save(commit=False)
            # Assign comment to post
            comment.post = post
            # Save the comment to the database
            comment.save()
            # Add a success message to the request object
            messages.success(request, "Your comment has been added.")
        context = {
            'comment': comment,
        }
        return render(request, 'blog/post/comment.html', context)

    context = {
        'form': CommentForm(),
    }
    return render(request, 'blog/post/forms/comment_form.html', context)


# TODO:
# Enable prefix matching, for example:
# Searching for 'app' should return posts containing 'apple' and 'application'.
# Currently matches whole words only, for example:
# Searching for 'app' returns 0 results. Searching 'apple' returns 1 result.
def post_search(request):
    """
    Post search view.

    Renders a template of published blog posts that match a query string.
    Finds posts that contain the query in their title or body.

    Context variables:
        - `query` - The query string submitted by the user.
        - `results` - A QuerySet of Post objects, ordered by relevance.
    """

    query = None
    results = []

    if 'query' in request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body', 'summary')
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