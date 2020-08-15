#使用celery
from celery import Celery
from django.core.mail import send_mail

from dailyFresh import settings
import time
app = Celery('celery_tasks.task',broker='redis://192.168.177.129:6379/8')

@app.task
#定义任务函数
def send_register_active_email(to_email,user_name,token):
    """发送激活邮件"""
    #组织邮件信息
    subject = "天天生鲜欢迎信息"
    # message = "<h1>{},欢迎您成为天天生鲜注册会员<h1>请点击以下链接激活您的账户<br/><a href='http://127.0.0.1:8000/user/active/{}'>http://127.0.0.1:8000/user/active/{}</a>".format(user_name,token,token)
    message = ''
    sender = settings.EMAIL_FROM  # 发件人
    recevier = [to_email]
    html_message = "<h1>{},欢迎您成为天天生鲜注册会员<h1>请点击以下链接激活您的账户<br/><a href='http://127.0.0.1:8000/user/active/{}'>http://127.0.0.1:8000/user/active/{}</a>".format(
        user_name, token, token)
    # message传输文本格式，html_message传输html格式的数据
    send_mail(subject, message, sender, recevier, html_message=html_message)
    time.sleep(5)