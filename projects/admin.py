from django.contrib import admin
from .models import Project, Screenshot


class ScreenshotInline(admin.TabularInline):
    model = Screenshot
    # Number of screenshots to display by default
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = ['id', 'slug', 'title', 'author', 'publish', 'status']
    # Column filters
    list_filter = ['status', 'created', 'publish', 'author']
    # Fields displayed in the admin edit form
    fields = ['slug', 'title', 'author', 'summary', 'description',
              'logo', 'publish', 'status']
    # Prepopulate slug field based on title
    prepopulated_fields = {'slug': ('title',)}
    # Order columns by status and publish date by default
    ordering = ['-status', '-publish']
    # Inline admin classes
    # Add or edit screenshots from the Project admin page
    inlines = [ScreenshotInline]


admin.site.register(Project, ProjectAdmin)