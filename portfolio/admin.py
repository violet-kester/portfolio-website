from django.contrib import admin
from .models import Project


admin.site.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = ['id', 'slug', 'title', 'author', 'publish', 'status']
    # Column filters
    list_filter = ['status', 'created', 'publish', 'author']
    # Fields displayed in the project edit form
    fields = ['slug', 'title', 'author', 'description',
              'thumbnail', 'publish', 'status']
    # Prepopulate slug field based on project title
    prepopulated_fields = {'slug': ('title',)}
    # Order columns by status and publish date by default
    ordering = ['-status', '-publish']
