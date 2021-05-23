import ssl
from qcloudsms_py import SmsMultiSender, SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import random
import smtplib
from email.mime.text import MIMEText
from UserRegister.models import User
import redis
from django.core.cache import cache
import json


# 发送短信
def send_sms_single(phone_num, template_id, template_param_list):
    """
    单条发送短信
    :param phone_num: 手机号
    :param template_id: 腾讯云短信模板ID
    :param template_param_list: 短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
    :return:
    """
    appid = 1400465479  # 自己应用ID
    appkey = "72a3879a1b3794ae0df9518dcff8f789"  # 自己应用Key
    sms_sign = "数学建模钉子户"  # 自己腾讯云创建签名时填写的签名内容（使用公众号的话这个值一般是公众号全称或简称）
    sender = SmsSingleSender(appid, appkey)
    try:
        response = sender.send_with_param(86, phone_num, template_id, template_param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': "网络异常发送失败"}
    return response


# 随机生成验证码
def gen_random_mobile_code(length=4):
    base_charts = '0123456789'
    return ''.join(random.choices(base_charts, k=length))


# 发送邮件
def send_mail(msg_to, verification_code):
    '''
    发送邮件
    :param msg_to: 收件方邮箱
    :param subject: 邮件主题
    :param content: 邮件内容
    :return:
    '''
    msg_from = '2239539295@qq.com'  # 发送方邮箱
    passwd = 'mkulnbcpudeqdijd'  # 填入发送方邮箱的授权码
    subject = 'DataSocial验证码'  # 主题设置为验证码
    content = '您的验证码为：' + str(verification_code) + str('，5分钟内有效。')

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        return 'success'
    except BaseException as e:
        print(e)
        return 'fail'
    finally:
        s.quit()


# 处理获取手机验证码
def deal_get_telephone_verification(tele_number, is_reg):
    '''
    :param tele_number: 电话号码
    :param is_reg: 判断是注册还是登录   True为注册 False为登录
    :return:
    '''
    if is_reg == False:  # 登录
        if User.objects.filter(telephone=tele_number).exists() == False:  # 不存在这个手机号
            data = {"info_head": 'fail_03', 'info_content': '该手机号未注册', 'extra_message': {}}
            return 'fail_03', data
    else:  # 注册
        if User.objects.filter(telephone=tele_number).exists():  # 已经注册改电话号码
            data = {"info_head": 'fail_01', 'info_content': '该电话号码已注册', 'extra_message': {}}
            return 'fail_01', data
    try:
        # 随机创建验证码
        random_mobile_code = gen_random_mobile_code()
        # redis存储 时长最长为300秒
        cache.set(tele_number, random_mobile_code, 300)
        # 腾讯云模板id
        tenxunyun_template_id = 820734
        send_sms_single(tele_number, tenxunyun_template_id, [random_mobile_code, ])
        data = {"info_head": 'success_01', 'info_content': '验证码已发送', 'extra_message': {}}
        return 'success_01', data
    except BaseException as e:
        data = {"info_head": 'fail_02', 'info_content': '短信发送失败', 'extra_message': {}}
        return 'fail_02', data


# 手机验证码核对
def check_telephone_verification(tele_number, verification, is_reg):
    '''

    :param tele_number:电话号码
    :param verification:验证码
    :param is_reg:是否为注册
    :return:
    '''
    if is_reg == True:  # 注册
        if User.objects.filter(telephone=tele_number).exists():  # 手机号码已注册
            data = {"info_head": 'fail_01', 'info_content': '该电话号码已注册', 'extra_message': {}}
            return 'fail_01', data
        if cache.has_key(tele_number) and cache.get(tele_number) == verification:  # 验证码存在并且匹配
            # 存储用户
            user = User(telephone=tele_number)
            user.save()
            # 查询用户的id并作为cookie放到客户端
            user_id = User.objects.values("id").filter(telephone=tele_number).first().get('id')
            # 返回注册成功页面,并将cookie传递到客户端中
            data = {"info_head": 'success_02', 'info_content': '注册成功，即将跳转页面',
                    'extra_message': {'tolink': '/account/register/reg_success/', "user_id": user_id,
                                      'cookie_day': 3}}
            return 'success_02', data
        else:
            # 验证码错误或者手机号错误
            data = {"info_head": 'fail_03', 'info_content': '验证码错误，重新填写',
                    'extra_message': {}}
            return 'fail_03', data
    else:  # 登录
        if User.objects.filter(telephone=tele_number).exists() == False:  # 手机号码未注册
            data = {"info_head": 'fail_04', 'info_content': '该手机号未注册', 'extra_message': {}}
            return 'fail_04', data
        if cache.has_key(tele_number) and cache.get(tele_number) == verification:  # 验证码存在并且匹配
            # 查询用户的id并作为cookie放到客户端
            user_id = User.objects.values("id").filter(telephone=tele_number).first().get('id')
            # 返回注册成功页面,并将cookie传递到客户端中
            data = {"info_head": 'success_03', 'info_content': '登录成功',
                    'extra_message': {'tolink': '/', "user_id": user_id,
                                      'cookie_day': 3}}
            return 'success_03', data
        else:  # 验证码不匹配或者不存在
            data = {"info_head": 'fail_03', 'info_content': '验证码错误，重新填写',
                    'extra_message': {}}
            return 'fail_03', data


# 处理邮箱登录和邮箱注册获取验证码
def deal_get_email_verification(email_num, is_reg):
    '''
    :param email_num:
    :param is_reg:
    :return:
    '''
    if is_reg == True:  # 注册
        if User.objects.filter(email=email_num).exists():  # 该用户已经注册
            data = {"info_head": 'fail_02', 'info_content': '该邮箱已被注册',
                    'extra_message': {}}
            return 'fail_02', data
        else:  # 该用户未注册
            verification_code = gen_random_mobile_code()
            email_send_is_success = send_mail(email_num, verification_code)
            if email_send_is_success == 'success':  # 邮件发送成功
                # redis存储验证码
                cache.set(email_num, verification_code, 300)
                data = {"info_head": 'success_01', 'info_content': '邮箱验证码已经成功发送',
                        'extra_message': {}}
                return 'success_01', data
            else:  # 邮件发送失败
                data = {"info_head": 'fail_01', 'info_content': '邮箱验证码发送失败，重新尝试发送',
                        'extra_message': {}}
                return 'fail_01', data
    else:  # 登录
        if User.objects.filter(email=email_num).exists() == False:  # 该用户未注册
            data = {"info_head": 'fail_04', 'info_content': '该邮箱未注册',
                    'extra_message': {}}
            return 'fail_04', data
        else:
            verification_code = gen_random_mobile_code()
            email_send_is_success = send_mail(email_num, verification_code)
            if email_send_is_success == 'success':  # 邮件发送成功
                # redis存储验证码
                cache.set(email_num, verification_code, 300)
                data = {"info_head": 'success_01', 'info_content': '邮箱验证码已经成功发送',
                        'extra_message': {}}
                return 'success_01', data
            else:  # 邮件发送失败
                data = {"info_head": 'fail_01', 'info_content': '邮箱验证码发送失败，重新尝试发送',
                        'extra_message': {}}
                return 'fail_01', data


# 邮箱登录和邮箱注册的表单验证码
def check_email_verification(email_num, verification, is_reg):
    '''
    :param tele_number:
    :param is_reg:
    :return:
    '''
    if is_reg == True:  # 注册
        # 判断邮箱是否注册
        if User.objects.filter(email=email_num).exists():  # 该用户已经注册
            data = {"info_head": 'fail_02', 'info_content': '该邮箱已被注册',
                    'extra_message': {}}
            return 'fail_02', data
        verification_code = gen_random_mobile_code()
        email_send_is_success = send_mail(email_num, verification_code)
        if email_send_is_success == 'success':  # 邮件发送成功
            # redis存储验证码
            cache.set(email_num, verification_code, 300)
            data = {"info_head": 'success_01', 'info_content': '邮箱验证码已经成功发送',
                    'extra_message': {}}
            return 'success_01', data
        else:  # 邮件发送失败
            data = {"info_head": 'fail_01', 'info_content': '邮箱验证码发送失败，重新尝试发送',
                    'extra_message': {}}
            return 'fail_01', data
    else:  # 登录
        if User.objects.filter(email=email_num).exists() == False:  # 没注册
            data = {"info_head": 'fail_04', 'info_content': '该邮箱未注册', 'extra_message': {}}
            return 'fail_04', data
        if cache.has_key(email_num) and cache.get(email_num) == verification:  # 验证码存在并且匹配
            # 查询用户的id并作为cookie放到客户端
            user_id = User.objects.values("id").filter(email=email_num).first().get('id')
            # 返回注册成功页面,并将cookie传递到客户端中
            data = {"info_head": 'success_03', 'info_content': '注册成功，即将跳转页面',
                    'extra_message': {'tolink': '/', "user_id": user_id,
                                      'cookie_day': 3}}
            return 'success_02', data
        else:
            # 验证码错误或者邮件号码错误
            data = {"info_head": 'fail_03', 'info_content': '验证码错误，重新填写',
                    'extra_message': {}}
            return 'fail_03', data

#密码登录表单验证
def check_password_sign(name,password):
    if User.objects.filter(name=name).exists()==False:#用户不存在
        data = {"info_head": 'fail_04', 'info_content': '该用户不存在', 'extra_message': {}}
        return 'fail_04', data
    else:
        if User.objects.values('password').filter(name=name).first().get('password')==password:#密码正确
            # 查询用户的id并作为cookie放到客户端
            user_id = User.objects.values("id").filter(name=name).first().get('id')
            # 返回注册成功页面,并将cookie传递到客户端中
            data = {"info_head": 'success_03', 'info_content': '登录，即将跳转页面',
                    'extra_message': {'tolink': '/', "user_id": user_id,
                                      'cookie_day': 3}}
            return 'success_02', data
        else:#密码错误
            data = {"info_head": 'fail_03', 'info_content': '密码错误，重新填写',
                    'extra_message': {}}
            return 'fail_03', data

