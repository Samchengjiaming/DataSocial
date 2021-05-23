"""DataSocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django.urls
from django.urls import path
from UserRegister import views

app_name='UserRegister'
urlpatterns = [
    #登录页面url
    path("sign_in/",views.sign_in,name='sign_in'),
    #注册页面url
    path("register/",views.register,name='register'),
    #使用邮箱注册
    path('register/with_email/',views.reg_email,name='reg_email'),
    #使用手机号注册
    path('register/with_telephone/',views.reg_phone,name='reg_phone'),
    #密码注册
    path('register/with_password/',views.reg_password,name='reg_password'),
    #手机号注册检查
    path('register/with_telephone_check/',views.reg_phone_check,name='reg_phone_check'),
    #密码注册检查
    path('register/with_password_check/',views.reg_password_check,name='reg_password_check'),
    #邮箱注册检查
    path('register/with_email_check/',views.reg_email_check,name='reg_email_check'),
    #注册成功页面
    path('register/reg_success/',views.reg_success,name='reg_success'),
    #邮箱登录
    path('sign_in/with_email/',views.sign_with_email,name='sign_with_email'),
    #手机号登录
    path('sign_in/with_phone/',views.sign_with_phone,name='sign_with_phone'),
    #账号登录
    path('sign_in/with_paasword/',views.sign_with_password,name='sign_with_password'),
    #登录检查
    path('sign_in/sign_check/',views.sign_check,name='sign_check'),
    # 退出登录
    path('logout/', views.logout, name='logout'),
    #bootstrap测试
    path('test/',views.test,name='test'),
]
