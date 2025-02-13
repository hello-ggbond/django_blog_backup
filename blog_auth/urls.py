from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse
from . import views


app_name = 'blog_auth'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('auth/login', views.blog_login, name='blog_login'),
    path('auth/logout', views.blog_logout, name='blog_logout'),
    path('auth/register', views.blog_register, name='blog_register'),
    path('auth/captcha', views.send_email_captcha, name='captcha'),
]