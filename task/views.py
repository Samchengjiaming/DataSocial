from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import random
from task.tool import check_task_title,task_dataset_file_save,save_task_dataset_info,status_select_task
import json
from django.core.paginator import Paginator
from task.models import TaskInfo,JoinTask
from django.db.models import Q
# Create your views here.

#任务列表页
def task_list(request,task_status='all',page=1):
    status_select_task_info=status_select_task(task_status)
    task_info_paginator = Paginator(status_select_task_info, 5)
    task_info_page = task_info_paginator.page(page)
    task_status=task_status
    return render(request,'task/task_list.html',locals())

#创建任务页面
def create_task(request):
    if request.COOKIES.get('user_id')==None:#用户没有登录
        return render(request, 'UserRegister/sign_in.html')
    #随机生成数据封路径、
    random_num=random.randint(1,16)
    if random_num<10:
        random_num_str='0'+str(random_num)
    else:
        random_num_str=str(random_num)
    dataset_img_path='/images/dataset/dataset_default_cover_img/default_dataset_img_'+random_num_str+'.jpg'
    return render(request,'task/create_task.html',context=locals())


#任务创建检查页面
def create_task_check(request):
    if request.is_ajax():  #异步提交表单
        post_data = request.POST  #表单数据
        #检查任务是否存在
        task_title = post_data.get("task_title")  #任务标题
        if check_task_title(task_title)==True:#任务标题已经存在
            response_data = {"info_head": 'fail_01', 'info_content': '任务标题已经存在',
                         'extra_message': {}}
            return JsonResponse(json.dumps(response_data),safe=False)
        task_dataset_file = request.FILES.get("task_dataset_file")
        # 任务数据集文件
        try:
            task_dataset_file_save(task_dataset_file,task_dataset_file.name,task_title)
        except Exception as e:
            print(e)#写入日志
            response_data={"info_head": 'fail_01', 'info_content': '数据集保存失败',
                        'extra_message': {}}
            return JsonResponse(json.dumps(response_data), safe=False)
        # 保存数据集信息
        user_id = request.COOKIES.get('user_id')
        if user_id== None:#用户未登录错误
            response_data={"info_head": 'error_02', 'info_content': '用户未登录错误',
                        'extra_message': {}}
            return JsonResponse(json.dumps(response_data), safe=False)
        try:
            save_task_dataset_info(post_data,user_id)
        except Exception as e:
            print(e)
            response_data = {"info_head": 'fail_02', 'info_content': '任务信息保存失败',
                             'extra_message': {}}
            return JsonResponse(json.dumps(response_data), safe=False)
        response_data = {"info_head": 'success', 'info_content': '任务保存成功',
                         'extra_message': {}}
        return JsonResponse(json.dumps(response_data), safe=False)


#任务详细页面
def task_info(request,task_id):
    user_id=request.COOKIES.get('user_id')
    is_join = JoinTask.objects.filter(Q(user_id=user_id) & Q(task_id=task_id)).exists()
    task_info=TaskInfo.objects.filter(task_id=task_id).first()
    return render(request,'task/task_info.html',locals())


#参加任务
def join_task(request,task_id):
    user_id=request.COOKIES.get('user_id')
    jointask=JoinTask(user_id=user_id,task_id=task_id,status=0)
    jointask.save()
    return redirect('/personal/homepage/collected_task/1')

