from django.contrib.postgres.search import SearchVector, SearchRank
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
        - `base_template`: The base template to extend from,
           depending on the request type.
    """

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        "base_template": base_template
    }
    return render(
        request,
        "blog/index.html",
        context,
    )


def post_detail(request, year, month, day, post):
    """
    Post detail view.

    Renders a template displaying a single published post,
    along with comments, a form for posting new comments,
    and a list of recommended posts.

    Parameters:
        - `year`: The year the post was published.
        - `month`: The month the post was published.
        - `day`: The day the post was published.
        - `post`: The post's unique slug identifier.

    Context variables:
       - `post`: The Post object representing the displayed post.
       - `comments`: A QuerySet of active comment objects related to the post.
       - `form`: An instance of the CommentForm for posting new comments.
       - `similar_posts`: A QuerySet of recommended Posts sharing common tags with the post.
       - `base_template`: The base template to extend from,
           depending on the request type.
    """

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    form = CommentForm()
    # Active comments for this post
    comments = post.comments.filter(active=True)
    # Similar, recommended posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(status='PB')\
                                .filter(tags__in=post_tags_ids)\
                                .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
        'base_template': base_template,
    }
    return render(request,
                  'blog/post/list.html',
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

    post_list = Post.objects.filter(status='PB')
    tag = None

    # If a tag slug is provided, filter posts by tag
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'posts': post_list,
        'tag': tag,
        'base_template': base_template,
    }
    return render(request,
                  'blog/post/list.html',
                  context)


def post_search(request):
    """
    Post search view.

    Renders a template of published blog posts that match a query string.
    Finds posts that contain the query in their title or body.

    Context variables:
        - `query` - The query string submitted by the user.
        - `results` - A QuerySet of Post objects, ordered by relevance.
        - `base_template`: The base template to extend from,
           depending on the request type.
    """

    query = None
    results = []

    if 'query' in request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Create a search vector based on title and body fields of posts
            search_vector = SearchVector('title', 'body')
            # Use the search vector and query to filter posts by status,
            # annotate posts with a search rank based on relevance,
            # and order posts by descending rank value
            results = Post.objects.filter(status='PB').annotate(
                search=search_vector,
                rank=SearchRank(search_vector, query)
            ).filter(search=query).order_by('-rank')

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'query': query,
        'results': results,
        'base_template': base_template,
    }
    return render(request,
                  'blog/post/list.html',
                  context)


def post_share(request, post_id):
    """
    Post share view.

    Allows users to share a published post by email using a form.
    Sends an email with a link to the post and optional message from the user.
    Renders a template with the post, form, and email status.

    Parameters:
        - `post_id`: The ID of the post.

    Context variables:
        - `post`: The Post object.
        - `form`: An instance of SharePostForm.
        - `sent`: A boolean indicating whether the email has been sent.
        - `base_template`: The base template to extend from,
           depending on the request type.
    """

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = SharePostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['senders_name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}" \
                      f"{data['senders_name']}\'s comments: {data['message']}"
            send_mail(subject, message,
                      'kester.violet.j@gmail.com', [data['to']])
            sent = True
    else:
        form = SharePostForm()

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'post': post,
        'form': form,
        'sent': sent,
        'base_template': base_template,
    }
    return render(request,
                  'blog/post/share_success.html',
                  context)


@require_POST
def post_comment(request, post_id):
    """
    Post comment view.

    Creates and displays a comment for a published post.
    Renders a template with success message and a link back to the post.

    Parameters:
        - `post_id`: The ID of the post being commented on.

    Context variables:
        - `post`: The Post object being commented on.
        - `base_template`: The base template to extend from,
           depending on the request type.
    """

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment without saving it to the database
        comment = form.save(commit=False)
        # Assign comment to post
        comment.post = post
        # Save the comment to the database
        comment.save()

    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'post': post,
        'base_template': base_template,
    }
    return render(request,
                  'blog/post/comment_success.html',
                  context)
