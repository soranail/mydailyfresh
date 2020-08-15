from django.contrib import admin
from django.urls import path, re_path

from apps.goods import views

app_name = 'goods'
urlpatterns = [
    re_path('',views.index,name='index')        #首页
    ]
