from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('posts/', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('posts/<slug:post_slug>', views.post_detail, name='post_detail'),
    path('posts/<slug:post_slug>/share/',
         views.post_share, name='post_share'),
    path('posts/<slug:post_slug>/comment/',
         views.post_comment, name='post_comment'),
    path('search/', views.post_search, name='post_search'),
]
