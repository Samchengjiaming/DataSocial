import os
from django.http import HttpResponse,JsonResponse
from dataset.tool import download_example_dataset,dataset_file_save,save_dataset_info
from dataset.tool import example_dataset_page_packing,check_dataset_title,check_lable_dataset
from django.shortcuts import render
import random
import json
from dataset.models import DatasetInfo,UserCollectDatasetHub
from django.core.paginator import Paginator

#首页样例数据下载
def example_dataset_download(request,index):
    example_index_list=[1,2,3]
    if index not in  example_index_list:
        return HttpResponse('资源不存在')
    else:
        file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/static/example/index_dataset/'
        print(file_path)
        if index==1:
            file_path=file_path+'phone7077.zip'
        if index==2:
            file_path=file_path+'bestsellers with categories.zip'
        if index==3:
            file_path=file_path+'Overflow2020.zip'
        file_response=download_example_dataset(file_path)
    return file_response

#首页样例数据详情页面
def example_dataset_info(request,index):
    example_index_list=[1,2,3]
    if index not in  example_index_list:
        return HttpResponse('资源不存在')
    else:
        example_dataset_info_page_render=example_dataset_page_packing(request,index)
        return example_dataset_info_page_render

#数据上传页面
def dataset_create(request):
    if request.COOKIES.get('user_id')==None:#用户没有登录
        return render(request, 'UserRegister/sign_in.html')
    #随机生成数据封路径、
    random_num=random.randint(1,16)
    if random_num<10:
        random_num_str='0'+str(random_num)
    else:
        random_num_str=str(random_num)
    dataset_img_path='/images/dataset/dataset_default_cover_img/default_dataset_img_'+random_num_str+'.jpg'
    return render(request,'Dataset/dataset_create.html',context=locals())

#数据上传检查函数
def dataset_create_check(request):
    if request.is_ajax():#异步提交表单
        post_data = request.POST #表单数据
        #检查数据集名称是否存在
        dataset_title=post_data.get("dataset_title")#数据集标题
        if check_dataset_title(dataset_title)==True:#数据集标题已经存在
            response_data = {"info_head": 'fail_02', 'info_content': '数据集标题已经存在',
                         'extra_message': {}}
            return JsonResponse(json.dumps(response_data),safe=False)
        dataset_file=request.FILES.get("dataset_file")
        #保存数据集文件
        try:
            dataset_file_save(dataset_file,dataset_file.name,dataset_title)
        except Exception as e:
            print(e)#写入日志
            response_data={"info_head": 'fail_01', 'info_content': '数据集保存失败',
                        'extra_message': {}}
            return JsonResponse(json.dumps(response_data), safe=False)
        #保存数据集信息
        user_id = request.COOKIES.get('user_id')
        if user_id== None:#用户未登录错误
            response_data={"info_head": 'error_02', 'info_content': '用户未登录错误',
                        'extra_message': {}}
            return JsonResponse(json.dumps(response_data), safe=False)
        try:
            save_dataset_info(post_data,user_id)
        except Exception as e:
            print(e)#写入日志
            response_data = {"info_head": 'fail_03', 'info_content': '数据信息保存失败',
                             'extra_message': {}}
            return JsonResponse(json.dumps(response_data), safe=False)
        #成功完成数据集的提交创建
        response_data = {"info_head": 'success', 'info_content': '数据集创建成功',
                         'extra_message': {'index_href':'/'}}
        return JsonResponse(json.dumps(response_data), safe=False)
    else:
        response_data = {"info_head": 'error_01', 'info_content': '错误',
                         'extra_message': {}}
        return JsonResponse(json.dumps(response_data), safe=False)


#数据集页面
def dataset_list(request,lable="recommend",page=1):#默认为推荐分类第一页
    if request.is_ajax():
        data=request.POST
        user_id=data.get('user_id')
        coolect_dataset_id=data.get('dataset_id')
        try:
            user_collect_dataset=UserCollectDatasetHub(user_id=user_id,collect_dataset_id=coolect_dataset_id)
            user_collect_dataset.save()
        except Exception:
            response_data = {"info_head": 'fail_01', 'info_content': '收藏数据集失败',
                         'extra_message': {}}
            return JsonResponse(json.dumps(response_data), safe=False)
        response_data = {"info_head": 'success_01', 'info_content': '收藏数据集成功',
                         'extra_message': {}}
        return JsonResponse(json.dumps(response_data), safe=False)
    else:
        if request.COOKIES.get('user_id'):#登录的用户，加载页面呈现已收藏数据的
            user_id=request.COOKIES.get('user_id')
            collect_dataset=UserCollectDatasetHub.objects.filter(user_id=user_id).values('collect_dataset_id')
            dataset_info_set, dataset_set_background, dataset_set_lables = check_lable_dataset(lable)
            dataset_info_paginator = Paginator(dataset_info_set, 5)
            dataset_info_page = dataset_info_paginator.page(page)
            lable = lable
            return render(request, 'Dataset/dataset_list.html', context=locals())
        else:
            dataset_info_set, dataset_set_background, dataset_set_lables = check_lable_dataset(lable)
            dataset_info_paginator = Paginator(dataset_info_set, 5)
            dataset_info_page = dataset_info_paginator.page(page)
            lable = lable
            return render(request, 'Dataset/dataset_list.html', context=locals())



def test(request):
    return HttpResponse('数据集app测试')
