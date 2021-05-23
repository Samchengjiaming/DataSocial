from homepage.models import UserInfo,User,DatasetInfo,DatasetInfoBackground,DatasetInfoLabels,UserCollectDatasetHub,TaskInfo,JoinTask,TaskAnswer
from django.http import HttpResponse, JsonResponse
import json
import os
from django.conf import settings

#保存用户信息
def save_user_info(post_data,user_id):
    user_name=post_data.get('user_name')
    user_signature=post_data.get('user_signature')
    user_place=post_data.get('user_place')
    user_school_or_company=post_data.get("user_school_or_company")
    user_major_or_position=post_data.get('user_major_or_position')
    user_personal_web=post_data.get('user_personal_web')
    #存储
    try:
        user=User.objects.get(id=user_id)
        user.name=user_name
        user.save()
        user_info=UserInfo(id=user_id,school_or_company=user_school_or_company,major_or_position=user_major_or_position,place=user_place,personal_web=user_personal_web,signature=user_signature)
        user_info.save()
    except Exception as e:#保存信息失败
        data = {"info_head": 'fail_01', 'info_content': '用户信息保存失败',
                'extra_message': {'tolink': '/personal/homepage/', "user_id": user_id,}}
        return JsonResponse(json.dumps(data), safe=False)
    data = {"info_head": 'success_01', 'info_content': '用户信息保存成功',
            'extra_message': {'tolink': '/personal/homepage/', "user_id": user_id, }}
    return JsonResponse(json.dumps(data), safe=False)


#查找用户发布的数据
def select_label_dataset(label,user_id):
    if label=='pub_dataset':#查找自己上传的数据
        select_dataset=DatasetInfo.objects.filter(author_id=user_id)
        select_dataset_id=select_dataset.values('dataset_id')
        select_dataset_background=DatasetInfoBackground.objects.filter(dataset_info_background_id__in=select_dataset_id)
        select_dataset_labels=DatasetInfoLabels.objects.filter(dataset_info_labels_id__in=select_dataset_id)
        return select_dataset,select_dataset_background,select_dataset_labels
    if label=='collected_dataset':#收藏数据
        user_collected_dataset_hub = UserCollectDatasetHub.objects.filter(user_id=user_id)
        select_dataset_id = user_collected_dataset_hub.values('collect_dataset_id')
        select_dataset=DatasetInfo.objects.filter(dataset_id__in=select_dataset_id)
        select_dataset_background = DatasetInfoBackground.objects.filter(
            dataset_info_background_id__in=select_dataset_id)
        select_dataset_labels = DatasetInfoLabels.objects.filter(dataset_info_labels_id__in=select_dataset_id)
        return select_dataset, select_dataset_background, select_dataset_labels
    if label=='pub_task':#发布的任务
        selected_task=TaskInfo.objects.filter(author_id=user_id)
        return selected_task
    if label=='collected_task':#收藏的任务
        collected_task=JoinTask.objects.filter(user_id=user_id)
        collected_task_id=collected_task.values('task_id')
        selected_task=TaskInfo.objects.filter(task_id__in=collected_task_id)
        return selected_task

#保存任务答案数据集
def save_task_dataset_file(file,user_id,task_id):
    task_file_dir=os.path.join(settings.TASK_ANSWER_DATASET,task_id)#任务所有答案保存文件夹
    if not os.path.exists(task_file_dir):
        os.makedirs(task_file_dir)
    file_save_path = os.path.join(task_file_dir, task_id + '_' + user_id)
    with open(file_save_path, 'wb') as file_write:
        if file.multiple_chunks():
            for file_block in file.chunks():
                file_write.write(file_block)
        else:
            file_write.write(file.read())


#保存任务答案新信息
def save_task_answer_info(task_answer_info,user_id):
    task_id = task_answer_info.get('task_id')
    answer_describe = task_answer_info.get('answer_describe')
    answer_insufficient = task_answer_info.get('answer_insufficient')
    status = 0
    TaskAnswer(task_id=task_id,user_id=user_id,answer_describe=answer_describe,
               answer_insufficient=answer_insufficient,status=status).save()