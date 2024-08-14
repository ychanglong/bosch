from logging import exception

from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForms
from .forms import LoginForm
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()


# Create your views here.
@require_http_methods(['GET', 'POST'])
def zllogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember = form.cleaned_data.get("remember")
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                user.is_authenticated
                # 是否需要记住我
                if not remember:
                    request.session.set_expiry(0)
                # 如果点击了就什么都不做 就默认两周过期时间
                return redirect('/')
            else:
                print('邮箱或者密码错误')
                # form.add_error('email', '邮箱或者密码错误!')
                # return render(request, 'login.html', context={'form': form})
                return redirect(reverse('zlauth:login'))


def zllogout(request):
    logout(request)
    return redirect('/')

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForms(request.POST)
        if (form.is_valid()):
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('zlauth:login'))
        else:
            print(form.errors)
            return redirect(reverse('zlauth:register'))
            # return render(request, 'register.html', context={'form': form})


def send_email_captcha(request):
    # ？email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'message': '必须传递邮箱!'})
    # 生成验证码(取随机4位阿拉伯数字)
    captcha = "".join(random.sample(string.digits, 4))
    try:
        CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
        # send_mail(
        #     subject='BOSCH博客注册验证码',
        #     message=f"您的注册验证码是：{captcha}",
        #     recipient_list=[email],
        #     from_email=None
        # )
        return JsonResponse({'code': 200, 'message': '验证码发送成功', '验证码': captcha})
    except Exception as e:
        print(e)
        raise Exception({'code': 400, 'message': '验证码发送败', '验证码:': captcha})
