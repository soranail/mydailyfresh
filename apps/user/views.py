import re
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer      #加密
from itsdangerous import SignatureExpired           #链接过期
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.core.urlresolvers import reverse
# Create your views here.
from django.urls import reverse
from django.views import View

from apps.user.models import User

# def create_user(request):
#     if request.method == 'GET':
#         return render(request,'create_user.html')
#     else:
#         return render(request,'test.html')
from celery_task.task import send_register_active_email


def test(request):
    return render(request,'test.html')

class RegisterView(View):
    """注册"""
    def get(self,request):
        """显示注册页面"""
        return render(request,'register.html')
    def post(self,request):
        """进行注册处理"""
        # 接收数据
        user_name = request.POST.get('user_name')
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")
        if allow != 'on':
            return render(request, "register.html", {'errmsg': "请同意协议"})
        # 数据效验
        if not all([user_name, password, email]):
            return render(request, "register.html", {'errmsg': "数据不完整"})
        # 验证邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',
                        email):
            return render(request, "register.html", {'errmsg': "邮箱错误"})
        # 检验用户名是否重复
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, "register.html", {'errmsg': "用户名已存在"})
        # 业务处理
        user = User.objects.create_user(user_name, email, password)
        user.is_active = 0          #未激活
        user.save()

        #发送激活邮件，包含激活链接，链接中要有密文信息
        #加密用户的身份信息，生成token
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        #默认的token为bytes类型，将其转为字符串
        token = token.decode()
        #发邮件
        send_register_active_email.delay(email,user_name,token)

        # 返回处理
        # return redirect('/goods/index')
        return redirect(reverse('goods:index'))

class ActiveView(View):
    """用户激活"""
    def get(self,request,token):
        #进行解密获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']

            #根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            #跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            #激活链接已过期
            return HttpResponse('激活链接已过期')

class LoginView(View):
    """登录"""
    def get(self,request):
        """显示登录页面"""
        return render(request,'login.html')

