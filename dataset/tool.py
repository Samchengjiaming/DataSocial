from django.http import FileResponse
from django.shortcuts import render
import json
import os
from django.conf import settings
from dataset.models import DatasetInfo,DatasetInfoBackground,DatasetInfoIntroduce,DatasetInfoLabels
from django.db.models import Q,F
from itertools import chain
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

#示例首页数据详情页面封装函数
def example_dataset_page_packing(request,index):
    file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/static/example/index_dataset/example_dataset_info.json'
    with open(file_path,'r',encoding='utf-8') as json_file:
        json_file_list=json.load(json_file)
        for example_dataset_info_dict in json_file_list:
            if example_dataset_info_dict['index']==index:
                return render(request,'Dataset/dataset_introduce.html',context=example_dataset_info_dict)

#数据集文件存储方法
def dataset_file_save(file,file_name,dataset_title):
    file_save_path=os.path.join(settings.DATASET_FILE_SAVE_ROOT,dataset_title+'_'+file_name)
    with open(file_save_path,'wb') as file_write:
        if file.multiple_chunks():
            for file_block in file.chunks():
                file_write.write(file_block)
        else:
            file_write.write(file.read())

#数据集名称检查
def check_dataset_title(dataset_title):
    '''
    :param dataset_title:
    :return: True 表示数据集名称已经存在
    '''
    if DatasetInfo.objects.filter(dataset_title=dataset_title).exists():#数据集标题已经存在
        return True
    else:
        return False

#按照label查找数据
def label_select_dataset(label):
    #all  分支
    if label=='all':
        dataset_set_info = DatasetInfo.objects.all()
        dataset_set_lables = DatasetInfoLabels.objects.all()
        dataset_set_background = DatasetInfoBackground.objects.all()
        return dataset_set_info, dataset_set_background, dataset_set_lables
    else:
        sub_label_dict = {'cv': ['面部识别', '图像分类', '目标检测', '姿态检测', '行为识别', '语义分割'],
                          'nlp': ['智能问答', "机器翻译", "文本分类", "情感分析", "语音识别", "文本生成"],
                          'td': ["共享汽车", "交通网络", "共享单车", "轨迹数据", "轨道数据", "出租车"],
                          'ml': ["社交网络", "复杂网络", "时间序列", "回归", "聚类", "分类"]}
        sub_label = sub_label_dict[label]
        select_lable_1_id = DatasetInfoLabels.objects.filter(
            Q(dataset_info_label_1=sub_label[0]) | Q(dataset_info_label_1=sub_label[1]) | Q(
                dataset_info_label_1=sub_label[2]) | Q(
                dataset_info_label_1=sub_label[3]) | Q(dataset_info_label_1=sub_label[4]) | Q(
                dataset_info_label_1=sub_label[5])).values(
            'dataset_info_labels_id')
        select_lable_2_id = DatasetInfoLabels.objects.filter(
            Q(dataset_info_label_2=sub_label[0]) | Q(dataset_info_label_2=sub_label[1]) | Q(
                dataset_info_label_2=sub_label[2]) | Q(
                dataset_info_label_2=sub_label[3]) | Q(dataset_info_label_2=sub_label[4]) | Q(
                dataset_info_label_2=sub_label[5])).values(
            'dataset_info_labels_id')
        select_lable_3_id = DatasetInfoLabels.objects.filter(
            Q(dataset_info_label_3=sub_label[0]) | Q(dataset_info_label_3=sub_label[1]) | Q(
                dataset_info_label_3=sub_label[2]) | Q(
                dataset_info_label_3=sub_label[3]) | Q(dataset_info_label_3=sub_label[4]) | Q(
                dataset_info_label_3=sub_label[5])).values(
            'dataset_info_labels_id')
        select_lable_id = select_lable_1_id | select_lable_2_id
        select_lable_id = select_lable_id | select_lable_3_id
        dataset_set_info = DatasetInfo.objects.filter(dataset_id__in=select_lable_id)
        dataset_set_lables = DatasetInfoLabels.objects.filter(dataset_info_labels_id__in=select_lable_id)
        dataset_set_background = DatasetInfoBackground.objects.filter(dataset_info_background_id__in=select_lable_id)
        return dataset_set_info, dataset_set_background, dataset_set_lables



#返回数据集类型
def check_lable_dataset(lable):
    if lable=='recommend':#为推荐数据
        dataset_set_info=DatasetInfo.objects.filter(recommend=1).order_by('dataset_id')
        dataset_set_id=dataset_set_info.values('dataset_id')
        dataset_set_lables=DatasetInfoLabels.objects.filter(dataset_info_labels_id__in=dataset_set_id)
        dataset_set_background = DatasetInfoBackground.objects.filter(dataset_info_background_id__in=dataset_set_id)
        return dataset_set_info,dataset_set_background,dataset_set_lables
    else:#按照label选择数据
        return label_select_dataset(lable)



#保存数据集信息
def save_dataset_info(dataset_info_dict,user_id):
    dataset_img=dataset_info_dict.get('dataset_img')#数据封面图片链接,
    dataset_background=dataset_info_dict.get('dataset_background')#数据背景
    dataset_introduce=dataset_info_dict.get('dataset_introduce')#数据集属性介绍
    dataset_sources=dataset_info_dict.get('dataset_sources')#数据来源,
    dataset_private=dataset_info_dict.get('dataset_private')#数据集权限,
    dataset_title=dataset_info_dict.get('dataset_title')#数据标题,
    select_lable_num=dataset_info_dict.get('select_lable_mun')#数据集标签数量,
    dataset_info=DatasetInfo(dataset_title=dataset_title,data_sources=dataset_sources,dataset_private=dataset_private,
                             dataset_img_path=dataset_img,dataset_path=dataset_title,author_id=user_id,favour=0)
    dataset_info.save()
    #dataset_info_label=dataset_info_dict.get("select_lable_"+str(index))
    if int(select_lable_num)==0:
        DatasetInfoLabels(dataset_info_labels_id=dataset_info.dataset_id).save()
    if int(select_lable_num)==1:
        DatasetInfoLabels(dataset_info_labels_id=dataset_info.dataset_id,dataset_info_label_1=dataset_info_dict.get("select_lable_0")).save()
    if int(select_lable_num)==2:
        DatasetInfoLabels(dataset_info_labels_id=dataset_info.dataset_id,dataset_info_label_1=dataset_info_dict.get("select_lable_0"),dataset_info_label_2=dataset_info_dict.get('select_lable_1')).save()
    if int(select_lable_num)==3:
        DatasetInfoLabels(dataset_info_labels_id=dataset_info.dataset_id,dataset_info_label_1=dataset_info_dict.get("select_lable_0"),dataset_info_label_2=dataset_info_dict.get('select_lable_1'),dataset_info_label_3=dataset_info_dict.get('select_lable_2')).save()
    DatasetInfoIntroduce(dataset_info_introduce_id=dataset_info.dataset_id,dataset_info_introduce_content=dataset_introduce).save()
    DatasetInfoBackground(dataset_info_background_id=dataset_info.dataset_id,dataset_info_background_content=dataset_background).save()