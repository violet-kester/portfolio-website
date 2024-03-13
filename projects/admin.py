from django.contrib import admin
from .models import Link, Project, Screenshot, Technology


class LinkInline(admin.TabularInline):
    model = Link
    # Set the order columns appear in the table
    fields = ('name', 'url', 'bootstrap_icon')
    # Number of empty slots to display (default is 3)
    extra = 1


class ScreenshotInline(admin.TabularInline):
    model = Screenshot
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = ['id', 'slug', 'title', 'created', 'status']
    # Column filters
    list_filter = ['status', 'created', 'created', 'author']
    # Fields displayed in the admin edit form
    fields = ['slug', 'title', 'subtitle', 'author', 'overview', 'technologies',
              'features', 'logo', 'thumbnail', 'created', 'status']
    # Prepopulate slug field based on title
    prepopulated_fields = {'slug': ('title',)}
    # Order columns by status and publish date by default
    ordering = ['-status', '-created']
    # Inline admin classes
    # Add or edit screenshots from the Project admin page
    inlines = [ScreenshotInline, LinkInline]


admin.site.register(Project, ProjectAdmin)


class TechnologyAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = ['name', 'category']


admin.site.register(Technology, TechnologyAdmin)
