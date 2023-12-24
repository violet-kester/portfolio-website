from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class Post(models.Model):
    """A model class that represents a post in a blog."""

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='blog/static/img/thumbnails/',
                                  default='static/img/logos/logo-thumbnail.png')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the absolute URL of the post detail view."""

        return reverse('blog:post_detail',
                       args=[self.slug])


class Comment(models.Model):
    """A model class that represents a comment on a post."""

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # For manually deactivating comments using the admin page
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
