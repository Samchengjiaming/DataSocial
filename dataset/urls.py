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
from dataset import views

app_name = 'Dataset'
urlpatterns = [
    # 测试
    path('test/', views.test, name='test'),
    # 首页样例数据下载界面
    path("example_dataset_download/<int:index>/", views.example_dataset_download, name="example_dataset_download"),
    # 首页样例数据详情页面
    path("example_dataset_info/<int:index>/",views.example_dataset_info,name="example_dataset_info"),
    #数据上传页面
    path('dataset_create/',views.dataset_create,name='dataset_create'),
    #上传数据集检查页面
    path('dataset_create_check/',views.dataset_create_check,name='dataset_create_check'),
    #数据集页面  首次加载默认界面
    path('dataset_list/',views.dataset_list,name='dataset_list'),
    #数据集页面带数据集标签和分页页数
    path('dataset_list/<lable>/<int:page>/',views.dataset_list,name='dataset_list'),
]
