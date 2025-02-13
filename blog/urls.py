from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('home', views.home, name='home'),
    path('blog', views.index, name='index'),
    path('blog/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('blog/pub', views.blog_pub, name='blog_pub'),
    path('blog/comment', views.comment_pub, name='comment_pub'),
    path('blog/search', views.search_blog, name='search_blog'),
    path('community', views.blog_community, name='blog_community'),
]