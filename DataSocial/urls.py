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
from django.urls import include
from django.urls import path
from UserRegister import views
from django.views import static ##新增
from django.conf import settings ##新增
from django.conf.urls import url ##新增

urlpatterns = [
    # 网站首页
    path("", views.index, name='index'),
    #注册页面
    path('account/', include("UserRegister.urls")),
    #验证码
    path('captcha/',include('captcha.urls')),
    #数据集界面
    path('dataset/',include('dataset.urls')),
    #个人主页
    path('personal/',include('homepage.urls')),
    #任务中心
    path('task/',include('task.urls')),
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
]
