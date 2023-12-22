from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = ['id', 'slug', 'title', 'author', 'publish', 'status']
    # Column filters
    list_filter = ['status', 'created', 'publish', 'author']
    # Fields displayed in the admin edit form
    fields = ['slug', 'title', 'author', 'summary', 'body',
              'thumbnail', 'tags', 'publish', 'status']
    # Prepopulate slug field based on title
    prepopulated_fields = {'slug': ('title',)}
    # Order columns by status and publish date by default
    ordering = ['-status', '-publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = ['name', 'post', 'created', 'active']
    # Column filters
    list_filter = ['active', 'created', 'updated']
