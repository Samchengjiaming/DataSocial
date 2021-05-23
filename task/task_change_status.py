from task.models import TaskInfo
import datetime
#判断任务状态
def task_change_status():
    print('------------'+str(datetime.datetime.now().strftime('%Y-%m-%d')+'------------'))
    print()
    not_begin_task_status_change=0
    begin_task_status_change=0
    #未开始
    not_begin_task_set=TaskInfo.objects.filter(status=0)
    for not_begin_task in not_begin_task_set:
        if str(not_begin_task.begin_day) == datetime.datetime.now().strftime('%Y-%m-%d'):
            not_begin_task.status=1
            not_begin_task_status_change+=1
    #已开始
    begin_task_set = TaskInfo.objects.filter(status=1)
    for begin_task in begin_task_set:
        if str(begin_task.begin_day) > datetime.datetime.now().strftime('%Y-%m-%d'):
            begin_task.status=2
            begin_task_status_change+=1
    print('今日开始的任务有'+str(not_begin_task_status_change)+'个,今日结束的任务有'+str(begin_task_status_change)+'个。')
    print('------------------------------------')
    print()