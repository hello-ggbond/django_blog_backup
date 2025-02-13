from django.shortcuts import render, HttpResponse, redirect,reverse
from django.http.response import JsonResponse
import string, random
from django.core.mail import send_mail

from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User

User = get_user_model()


# Create your views here.
# @require_http_methods(['GET', 'POST'])
# def blog_login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     else:
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             remember = form.cleaned_data.get('remember')
#             user = User.objects.filter(email=email).first()
#             if user and user.check_password(password):
#                 login(request, user)
#                 if not remember:
#                     request.session.set_expiry(0)
#                 return redirect('blog:home')  # 成功后后访问的URL
#             else:
#                 error = '密码错误！！！'
#                 print(error)
#                 # form = form.errors
#                 # print(form)
#                 return render(request, 'login.html', {'form': form, 'error': error})
#                 # return JsonResponse({'code':400,'errors':'邮箱或密码输入错误！！！'})
#         else:
#             form = form.errors
#             print(form)
#             return render(request, 'login.html', {'form': form})
#             # return JsonResponse({'code':400, 'errors':'密码错误！！！'})
@require_http_methods(['GET', 'POST'])
def blog_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('blog:home')  # 成功后访问的URL
            else:
                # 邮箱或密码错误
                error = '邮箱或密码输入错误！！！'
                print(error, form)
                return render(request, 'login.html', {'form': form, 'error': error})
        else:
            # 表单验证失败（可能是空输入或其他验证错误）
            if not form.cleaned_data.get('email') or not form.cleaned_data.get('password'):
                error = '请输入邮箱或密码！！！'
            else:
                error = '表单格式输入有误，请检查！！！'
            return render(request, 'login.html', {'form': form, 'error': error})



def blog_logout(request):
    logout(request)
    return redirect('blog:home')


@require_http_methods(['GET','POST'])
def blog_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('blog_auth:blog_login'))
        # else:
        #     print(form.errors)
        #     form = form.errors
        #     return render(request, 'register.html', {"form": form})
            # return redirect(reverse('blog_auth:blog_register'))


def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code':400, 'message':'Defeat!!'})
    captcha = "".join(random.sample(string.digits, 4))
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha':captcha})  # 存储到数据库
    send_mail(subject='博客验证码', message=f'您的验证码为:{captcha}', from_email=None, recipient_list=[email])
    return JsonResponse({'code':200, 'message':'SUCCESS'})
