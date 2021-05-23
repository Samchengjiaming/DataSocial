from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from homepage.models import User,UserInfo,TaskAnswer,TaskInfo
from homepage.tool import save_user_info,select_label_dataset,save_task_dataset_file,save_task_answer_info
from django.core.paginator import Paginator
import json
from django.db.models import Q,F
from django.conf import settings
import os
from django.http import FileResponse

#个人主页
def homepage(request,label='collected_task',page=1):
    if request.COOKIES.get('user_id')==None:#用户没有登录
        return render(request, 'UserRegister/sign_in.html')
    else:
        user_id = request.COOKIES.get('user_id')
        # 查找姓名
        try:
            user_name = User.objects.filter(id=user_id).values('name')[0]
            user_info = UserInfo.objects.filter(id=user_id).values()[0]
        except IndexError:#存在用户没有修改过个人信息
            user_name, user_info = None, None
        if label=='pub_dataset' or label=='collected_dataset':
            dataset_info_set,dataset_set_background,dataset_set_lables=select_label_dataset(label,user_id)
            dataset_info_paginator = Paginator(dataset_info_set, 5)
            dataset_info_page = dataset_info_paginator.page(page)
            label = label
            return render(request, 'homepage/personal_homepage.html', locals())
        if label=='pub_task' or label=='collected_task':
            label=label
            task_info=select_label_dataset(label,user_id)
            task_info_paginator=Paginator(task_info, 5)
            task_info_page=task_info_paginator.page(page)
            return render(request,'homepage/personal_homepage.html',locals())


#个人信息修改页面
def personal_info_edit(request):
    if request.COOKIES.get('user_id')==None:#用户没有登录
        return render(request, 'UserRegister/sign_in.html')
    else:
        return render(request,'homepage/personal_info_edit.html')


#个人信息修改检查页面
def personal_info_edit_check(request):
    if request.is_ajax():
        if request.COOKIES.get('user_id') == None:  # 用户没有登录
            return render(request, 'UserRegister/sign_in.html')
        else:
            post_data = request.POST
            # 存储用户信息
            json_response = save_user_info(post_data, request.COOKIES.get('user_id'))
            return json_response

#提交任务页面
def submit_task_answer(request,task_id):
    task_id=task_id
    return render(request,'homepage/personal_submit_task_answer.html',locals())


def check_submit_task_answer(request):
    if request.is_ajax():  # 异步提交表单
        post_data = request.POST  # 表单数据
        task_id=post_data.get('task_id')
        user_id=request.COOKIES.get('user_id')
        dataset_file=request.FILES.get("task_dataset_file")
        #检查用户回答是否已经存在
        if TaskAnswer.objects.filter(Q(user_id=user_id) & Q(task_id=task_id)).exists():
            response_data={"info_head": 'fail_03', 'info_content': '您已经回答过该任务',
                        'extra_message': {}}
            return JsonResponse(json.dumps(response_data), safe=False)
        # 保存数据
        try:
            save_task_dataset_file(dataset_file,user_id,task_id)
        except Exception:
            print(e)#写入日志
            response_data={"info_head": 'fail_01', 'info_content': '答案数据集保存失败',
                        'extra_message': {}}
            return JsonResponse(json.dumps(response_data), safe=False)
        try:
            save_task_answer_info(post_data,user_id)
        except Exception:
            print(e)#写入日志
            response_data={"info_head": 'fail_02', 'info_content': '答案信息保存失败',
                        'extra_message': {}}
            return JsonResponse(json.dumps(response_data), safe=False)
        response_data = {"info_head": 'success_01', 'info_content': '提交成功',
                         'extra_message': {'herf':'/personal/homepage/collected_task/1'}}
        return JsonResponse(json.dumps(response_data), safe=False)

#查看任务答案
def task_answer_list(request,task_id):
    user_id=request.COOKIES.get('user_id')
    author_id=TaskInfo.objects.filter(task_id=task_id).values('author_id').first().get('author_id')
    if str(author_id)!=user_id:
        return HttpResponse('无权查看')
    else:
        task_answer_list=TaskAnswer.objects.filter(task_id=task_id)
        task_answer_list_count=task_answer_list.count()
        return render(request,'homepage/personal_task_answer_list.html',locals())

#任务答案详细
def task_answer_info(request,task_id,author_id):
    task_answer_info=TaskAnswer.objects.filter(Q(task_id=task_id) & Q(user_id=author_id)).first()
    return render(request,'homepage/personal_task_answer_info.html',locals())


#下载任务答案附件
def download_task_dataset(request,task_id,author_id):
    task_file_dir=os.path.join(settings.TASK_ANSWER_DATASET,task_id)
    file_save_path = os.path.join(task_file_dir, task_id + '_' + author_id)
    file_response=download_example_dataset(file_save_path)
    return file_response

#示例数据下载函数
def download_example_dataset(file_path):
    file_name=file_path.split('\\')[-1]
    file=open(file_path, 'rb')
    file_response = FileResponse(file)
    # 以流的形式下载文件,这样可以实现任意格式的文件下载
    file_response['Content-Type'] = 'application/octet-stream'
    # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
    file_response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
    return file_response