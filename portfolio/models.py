from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Project(models.Model):
    """A model class that represents a project in a portfolio."""

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
                               related_name='projects')
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='portfolio/static/images/thumbnails/',
                                  default='portfolio/static/images/thumbnails/default_thumbnail.png')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the absolute URL of the project detail view."""

        return reverse('portfolio:project_detail',
                       args=[self.slug])
