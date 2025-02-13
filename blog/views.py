from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from .apps import BlogConfig
from .models import BlogCategory, Blog, BlogComment
from .forms import BlogPubForm
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    blogs = Blog.objects.all()
    return render(request, 'blog.html', context={"blogs": blogs})

@login_required()
def blog_detail(request, blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id)
        except Exception as e:
            blog = None
            print("ERROR")
        return render(request, 'blog_detail.html', {'blog':blog})


# @login_required(login_url=reverse_lazy("zlauth:login"))
# @login_required(login_url="/auth/login")
@require_http_methods(['GET', 'POST'])
@login_required()
def blog_pub(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'blog_pub.html', context={"categories": categories})
    else:
        form = BlogPubForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            print(request.POST)
            print(request.POST.get('content'))
            return JsonResponse({"code": 200, "message": "博客发布成功！", "data": {"blog_id": blog.id}})
        else:
            print(request.POST)
            print(form.errors)
            return JsonResponse({'code': 400, "message": "参数错误！"})


@require_POST
@login_required(login_url='/auth/login')
def comment_pub(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(blog_id=blog_id, content=content, author=request.user)
    return redirect(reverse('blog:blog_detail', kwargs={'blog_id': blog_id}))

@require_GET
def search_blog(request):
    q = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'blog.html', {'blogs': blogs})


def blog_community(request):
    return render(request, 'community.html')
