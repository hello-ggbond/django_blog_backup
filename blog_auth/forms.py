from django import forms
from django.contrib.auth import get_user_model
from django.template.defaultfilters import length

from .models import CaptchaModel

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=10, min_length=2, error_messages={
        'required':'请输入用户名！',
        'max_length':'用户名长度在2-10之间',
        'min_length': '用户名长度在2-10之间'
    })
    email = forms.EmailField(error_messages={
        'required':'请输入邮箱名',
        'invalid':'请输入正确的邮箱格式'
    })
    captcha = forms.CharField(max_length=4, min_length=4, error_messages={'required':'请输入验证码！'})
    password = forms.CharField(max_length=10, min_length=2, error_messages={
        'required':'请输入密码！',
        'max_length':'用户名长度在2-10之间',
        'min_length': '用户名长度在2-10之间'
    })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已经存在！')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError('邮箱与验证码不匹配！')
        captcha_model.delete()
        return captcha



class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '请输入邮箱名！！！',
            'invalid': '请输入正确的邮箱格式！！！'
        }
    )
    password = forms.CharField(
        max_length=10,
        min_length=2,
        error_messages={
            'required': '请输入密码！！！',
            'max_length': '密码长度在2-10之间！',
            'min_length': '密码长度在2-10之间！'
        }
    )
    remember = forms.IntegerField(required=False)

    # 自定义全局表单验证
    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('email')
    #     password = cleaned_data.get('password')
    #
    #     if password == '':
    #         self.add_error('password', '您输入的密码为空！！！')
    #
    #     if email == '':
    #         self.add_error('email','邮箱必须填写！！！')
    #         raise forms.ValidationError('邮箱必须填写！！！')
    #
    #     if password != password:
    #         self.add_error('password','密码！！！')
    #         raise forms.ValidationError('密码错误！！！')

