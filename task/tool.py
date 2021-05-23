from task.models import TaskInfo
from django.conf import settings
import datetime
import os

#查询任务数据
def status_select_task(status):
    if status=='all':
        return TaskInfo.objects.all()
    if status=='not_begin':
        return TaskInfo.objects.filter(status=0)
    if status=='underway':
        return TaskInfo.objects.filter(status=1)
    if status=='end':
        return TaskInfo.objects.filter(status=2)

# 检查任务名称是否存在
def check_task_title(task_title):
    if TaskInfo.objects.filter(task_title=task_title).exists():
        return True
    else:
        return False


# 保存数据集
def task_dataset_file_save(file, file_name, dataset_title):
    file_save_path = os.path.join(settings.TASK_DATASET_FILE_SAVE_ROOT, dataset_title + '_' + file_name)
    with open(file_save_path, 'wb') as file_write:
        if file.multiple_chunks():
            for file_block in file.chunks():
                file_write.write(file_block)
        else:
            file_write.write(file.read())


# 保存数据集信息
def save_task_dataset_info(task_dataset_info_dict, user_id):
    task_title = task_dataset_info_dict.get('task_title')
    task_describe = task_dataset_info_dict.get('task_describe')
    task_require = task_dataset_info_dict.get('task_require')
    task_coin = task_dataset_info_dict.get('task_coin')
    task_day = int(task_dataset_info_dict.get('task_day'))
    dataset_img = task_dataset_info_dict.get('dataset_img')
    begin_day=task_dataset_info_dict.get('task_begin_day')
    deadline = (datetime.datetime.now() + datetime.timedelta(task_day)).strftime('%Y-%m-%d')
    if begin_day>datetime.datetime.now().strftime('%Y-%m-%d'):
        status=0#没有开始
    else:
        status=1#任务开始状态
    taskinfo = TaskInfo(task_title=task_title, task_describe=task_describe, task_require=task_require,
                         coin=task_coin,author_id=user_id,dataset_img_path=dataset_img,dataset_path=task_title,
                        deadline=deadline,begin_day=begin_day,status=status)
    taskinfo.save()

