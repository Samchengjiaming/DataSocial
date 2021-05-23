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
from homepage import views

app_name = 'homepage'
urlpatterns = [
    # 个人主页默认页面
    path('homepage/',views.homepage,name='homepage'),
    # 个人主页含参页面
    path('homepage/<label>/<int:page>/',views.homepage,name='homepage'),
    #个人信息修改默认页面
    path('personal_info_edit/',views.personal_info_edit,name='personal_info_edit'),
    #个人信息修改检查
    path("personal_info_edit_check/",views.personal_info_edit_check,name='personal_info_edit_check'),
    #提交任务答案页面
    path('submit_task_answer/<task_id>',views.submit_task_answer,name='submit_task_answer'),
    #提交任务检查
    path('check_submit_task_answer/',views.check_submit_task_answer,name='check_submit_task_answer'),
    #查看任务答案
    path('task_answer_list/<task_id>/',views.task_answer_list,name='task_answer_list'),
    #查看任务答案详细
    path('task_answer_info/<task_id>/<author_id>/',views.task_answer_info,name='task_answer_info'),
    #下载任务答案附件、
    path('download_task_dataset/<task_id>/<author_id>/',views.download_task_dataset,name='download_task_dataset'),
]
