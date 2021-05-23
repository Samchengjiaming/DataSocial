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
from task import views

app_name = 'task'
urlpatterns = [
    #任务列表默认页
    path('task_list/',views.task_list,name='task_list'),
    #任务列表带参数页
    path('task_list/<task_status>/<int:page>/',views.task_list,name='task_list'),
    #创建任务
    path('create_task/',views.create_task,name='create_task'),
    #任务创建检查函数
    path('create_task_check/',views.create_task_check,name='create_task_check'),
    #任务详细页面
    path('task_info/<task_id>/',views.task_info,name='task_info'),
    #用户参加任务
    path('join_task/<task_id>/',views.join_task,name='join_task'),
]
