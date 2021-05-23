from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from UserRegister.models import User
from UserRegister.forms import Reg_password_check
import time
import datetime
from UserRegister.tool import send_sms_single, gen_random_mobile_code, send_mail,deal_get_telephone_verification,check_telephone_verification
from UserRegister.tool import check_email_verification,deal_get_email_verification,check_password_sign
import redis
from django.core.cache import cache
import json


# Create your views here.

# 首页
def index(request):
    user_id=request.COOKIES.get('user_id')
    return render(request, "index.html",context=locals())

#退出登录
def logout(erquest):
    res=redirect('/')
    res.delete_cookie('user_id')
    return res

# 登录页面
def sign_in(request):
    return render(request, 'UserRegister/sign_in.html')


# 注册页面
def register(request):
    return render(request, 'UserRegister/register.html')


# 密码注册
def reg_password(request):
    form = Reg_password_check()
    return render(request, 'UserRegister/reg_password.html', context=locals())


# 手机注册页面
def reg_phone(request):
    return render(request, 'UserRegister/reg_phone.html')


# 邮箱注册页面
def reg_email(request):
    return render(request, 'UserRegister/reg_email.html')


# 注册成功页面
def reg_success(request):
    return render(request, 'UserRegister/reg_success.html')

#测试
def test(request):
    return render(request,'模板.html')

# 手机注册检查
def reg_phone_check(request):
    if request.is_ajax():  # ajax请求数据
        post_data = request.POST
        post_type = post_data.get('post_type')
        if post_type == 'get_verification':  # 请求验证码
            tele_number = post_data.get('tele_number')
            # 检查改电话号码是否已经注册
            if User.objects.filter(telephone=tele_number).exists():  # 已经注册改电话号码
                data = {"info_head": 'fail_01', 'info_content': '该电话号码已注册', 'extra_message': {}}
                return JsonResponse(json.dumps(data), safe=False)
            try:
                # 随机创建验证码
                random_mobile_code = gen_random_mobile_code()
                # redis存储 时长最长为300秒
                cache.set(tele_number, random_mobile_code, 300)
                tenxunyun_template_id = 820734
                send_sms_single(tele_number, tenxunyun_template_id, [random_mobile_code, ])
                data = {"info_head": 'success_01', 'info_content': '验证码已发送', 'extra_message': {}}
                return JsonResponse(json.dumps(data), safe=False)
            except BaseException as e:
                data = {"info_head": 'fail_02', 'info_content': '短信发送失败', 'extra_message': {}}
                return JsonResponse(json.dumps(data), safe=False)
        if post_type == 'form_post':  # 表单提交
            # 验证验证码是否正确
            tele_number = post_data.get('tele_number')
            verification = post_data.get('verification')
            if User.objects.filter(telephone=tele_number).exists():  # 手机号码已注册
                data = {"info_head": 'fail_01', 'info_content': '该电话号码已注册', 'extra_message': {}}
                return JsonResponse(json.dumps(data), safe=False)
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
                return JsonResponse(json.dumps(data), safe=False)
            else:
                # 验证码错误或者手机号错误
                data = {"info_head": 'fail_03', 'info_content': '验证码错误，重新填写',
                        'extra_message': {}}
                return JsonResponse(json.dumps(data), safe=False)
    else:  # 不是ajax请求,一般来说不会出现这种情况  前端只有ajax提交
        data = {"info_head": 'error_01', 'info_content': '系统内部错误',
                'extra_message': {}}
        return JsonResponse(json.dumps(data), safe=False)


# 密码注册检查
def reg_password_check(request):
    if request.method == 'POST':  # POST提交表示用户完整提交
        # 使用提交数据生成表单
        form = Reg_password_check(request.POST)
        if form.is_valid():  # 验证成功
            # 获取表单数据
            post_data = request.POST
            name = post_data.get('name')
            password = post_data.get('password')
            # 先存储用户记录
            user = User(name=name, password=password)
            user.save()
            # 查询用户的id并作为cookie放到客户端
            user_id = User.objects.values("id").filter(name=name).first().get('id')
            # 返回注册成功页面,并将cookie传递到客户端中
            response = redirect('/account/register/reg_success/')  # 先返回注册成功页面
            # 设置cookie过期时间为3天
            future = datetime.datetime.now() + datetime.timedelta(days=3)
            # 返回cookie至客户端
            response.set_cookie('user_id', user_id, expires=future)
            return response
        else:  # 验证不成功,把错误信息返回前端页面
            return render(request, 'UserRegister/reg_password.html', {'form': form})
    else:  # 不是POST提交，直接返回表单
        form = Reg_password_check()
    return render(request, 'UserRegister/reg_password.html', context={'form': form})


# 邮箱注册检查
def reg_email_check(request):
    if request.is_ajax():
        post_data = request.POST
        post_type = post_data.get('post_type')
        if post_type == 'get_verification':  # 请求发送邮件验证码
            email_num = post_data.get('email_num')
            # 判断邮箱是否注册
            if User.objects.filter(email=email_num).exists():  # 该用户已经注册
                data = {"info_head": 'fail_02', 'info_content': '该邮箱已被注册',
                        'extra_message': {}}
                return JsonResponse(json.dumps(data), safe=False)
            verification_code = gen_random_mobile_code()
            email_send_is_success = send_mail(email_num, verification_code)
            if email_send_is_success == 'success':  # 邮件发送成功
                # redis存储验证码
                cache.set(email_num, verification_code, 300)
                data = {"info_head": 'success_01', 'info_content': '邮箱验证码已经成功发送',
                        'extra_message': {}}
                return JsonResponse(json.dumps(data), safe=False)
            else:  # 邮件发送失败
                data = {"info_head": 'fail_01', 'info_content': '邮箱验证码发送失败，重新尝试发送',
                        'extra_message': {}}
                return JsonResponse(json.dumps(data), safe=False)
        if post_type == 'form_post':  # 提交表单
            email_num = post_data.get('email_num')
            verification = post_data.get('verification')
            if User.objects.filter(email=email_num).exists():  # 该邮箱已经注册
                data = {"info_head": 'fail_02', 'info_content': '该邮箱已被注册',
                        'extra_message': {}}
                return JsonResponse(json.dumps(data), safe=False)
            if cache.has_key(email_num) and cache.get(email_num) == verification:  # 验证码存在并且匹配
                # 存储用户
                user = User(email=email_num)
                user.save()
                # 查询用户的id并作为cookie放到客户端
                user_id = User.objects.values("id").filter(email=email_num).first().get('id')
                # 返回注册成功页面,并将cookie传递到客户端中
                data = {"info_head": 'success_02', 'info_content': '注册成功，即将跳转页面',
                        'extra_message': {'tolink': '/account/register/reg_success/', "user_id": user_id,
                                          'cookie_day': 3}}
                return JsonResponse(json.dumps(data), safe=False)
            else:
                # 验证码错误或者邮件号码错误
                data = {"info_head": 'fail_03', 'info_content': '验证码错误，重新填写',
                        'extra_message': {}}
                return JsonResponse(json.dumps(data), safe=False)
    else:  # 不是ajax提交
        data = {"info_head": 'error_01', 'info_content': '系统内部错误',
                'extra_message': {}}
        return JsonResponse(json.dumps(data), safe=False)


# 手机号登录页面
def sign_with_phone(request):
    return render(request, 'UserRegister/sign_phone.html')


# 邮箱登录
def sign_with_email(request):
    return render(request, 'UserRegister/sign_email.html')


# 账号登录
def sign_with_password(request):
    return render(request, 'UserRegister/sign_password.html')


# 登录检查
def sign_check(request):
    '''
    检查三种登录方式
    :param request:
    :return:
    '''
    if request.is_ajax():  # 异步请求
        post_data = request.POST
        post_type = post_data.get('post_type')
        if post_type=='get_telephone_verification':#请求发送手机验证码
            tele_number=post_data.get('tele_number')
            info_head,data=deal_get_telephone_verification(tele_number,is_reg=False)
            return JsonResponse(json.dumps(data),safe=False)
        if post_type=='telephone_form_post':#手机登录表单提交
            tele_number = post_data.get('tele_number')
            verification = post_data.get('verification')
            info_head,data=check_telephone_verification(tele_number,verification,is_reg=False)
            return JsonResponse(json.dumps(data),safe=False)
        if post_type=='get_email_verification':#请求发送邮件验证码
            email_num=post_data.get('email_num')
            info_head,data=deal_get_email_verification(email_num,is_reg=False)
            return JsonResponse(json.dumps(data),safe=False)
        if post_type=='email_form_post':
            email_num = post_data.get('email_num')
            verification = post_data.get('verification')
            info_head,data=check_email_verification(email_num, verification, is_reg=False)
            return JsonResponse(json.dumps(data),safe=False)
        if post_type=='password_form_post':
            name=post_data.get('name')
            password=post_data.get('password')
            info_head,data=check_password_sign(name,password)
            return JsonResponse(json.dumps(data),safe=False)
    else:  # 不是异步请求，内部错误
        data = {"info_head": 'error_01', 'info_content': '系统内部错误',
                'extra_message': {}}
        return JsonResponse(json.dumps(data), safe=False)


