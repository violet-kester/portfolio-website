from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Technology(models.Model):
    """A model class that represents a technology used in a project."""

    CATEGORY_CHOICES = [
        (1, "Backend framework"),
        (2, "Frontend framework"),
        (3, "Databases and persistence"),
        (4, "CSS framework"),
        (5, "Testing framework"),
        (6, "Misc."),
    ]
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=5)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['category', Lower('name')]
        verbose_name = 'Technology'
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    A model class that represents a project in a portfolio.

    Many-to-many relationship with:
        - Technologies

    One-to-many relationships with:
        - Links
        - Screenshots
    """

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='projects')
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    technologies = models.ManyToManyField(Technology, related_name='projects')
    logo = models.ImageField(upload_to='projects/img/logos/',
                             default='img/logos/portfolio-logo-480.png')
    thumbnail = models.ImageField(
        upload_to='projects/img/thumbnails/',
        default='img/logos/portfolio-logo-480.png'
    )
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

        return reverse('projects:project_detail',
                       args=[self.slug])


class Link(models.Model):
    """A model class that represents a link related to a project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='links'
    )
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=250)
    bootstrap_icon = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.project.title} link to {self.name}'


class Screenshot(models.Model):
    """A model class that represents a screenshot of a project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='screenshots'
    )
    image = models.ImageField(
        upload_to='projects/img/screenshots/'
    )
    description = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f'{self.project.title} screenshot {self.id}'
