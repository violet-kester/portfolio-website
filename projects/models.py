from django.contrib.auth.models import User
from django.db import models
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
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='projects/static/projects/img/logos/',
                             default='static/img/logos/logo-480.png')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the absolute URL of the project detail view.

        For example:
            project = Project.objects.get(slug='jobly')
            project.get_absolute_url()
        Returns:
            'https://example.com/projects/jobly/'
        """

        return reverse('portfolio:project_detail',
                       args=[self.slug])


class Screenshot(models.Model):
    """A model class that represents a screenshot of a project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='screenshots'
    )
    image = models.ImageField(
        upload_to='projects/static/projects/img/screenshots/'
    )

    def __str__(self):
        return f'Screenshot of {self.project.title}'
