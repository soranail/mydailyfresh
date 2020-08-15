from django.contrib import admin
from django.urls import path, re_path

from apps.user import views
from apps.user.views import RegisterView, ActiveView, LoginView

app_name = 'user'
urlpatterns = [
    # re_path('create_user',views.create_user,name='create_user'),
    # re_path("register/",views.register,name='register'),    #注册
    re_path('register/',RegisterView.as_view(),name='register'),  #类注册
    re_path('active/(?P<token>.*)',ActiveView.as_view(),name='active'),   #用户激活
    re_path('login/',LoginView.as_view(),name='login'),     #用户登录



    re_path('test',views.test,name='test'),
    ]
