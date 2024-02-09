from django.contrib import admin
from .models import Post, Comment, Banner

class BannerInline(admin.TabularInline):
    model = Banner

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = ['id', 'slug', 'title', 'author', 'publish', 'status']
    # Column filters
    list_filter = ['status', 'created', 'publish', 'author']
    # Fields displayed in the admin edit form
    fields = ['slug', 'title', 'subtitle', 'author', 'overview', 'body',
              'thumbnail', 'tags', 'publish', 'status']
    # Prepopulate slug field based on title
    prepopulated_fields = {'slug': ('title',)}
    # Order columns by status and publish date by default
    ordering = ['-status', '-publish']
    # Inline admin classes
    # Add or edit the banner image from the Post admin page
    inlines = [BannerInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = ['name', 'post', 'created', 'active']
    # Column filters
    list_filter = ['active', 'created', 'updated']

