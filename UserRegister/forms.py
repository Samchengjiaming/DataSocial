from django import forms
from captcha.fields import CaptchaField
from UserRegister.models import User

#密码注册验证
class Reg_password_check(forms.Form):
    name=forms.CharField(min_length=3,max_length=15,required=True,error_messages={
        'required':"用户名不能为空",
        'min_length':"用户名不能少于3个字符",
        'max_length':"用户名不能超过15个字符"
    })
    password=forms.CharField(min_length=6,max_length=15,required=True,error_messages={
        'required':"密码不能为空",
        'min_length':"密码不能少于6个字符",
        'max_length':"密码不能超过15个字符"
    })
    re_password=forms.CharField(min_length=6,max_length=15,required=True,error_messages={
        'required':"密码不能为空",
        'min_length':"密码不能少于6个字符",
        'max_length':"密码不能超过15个字符"
    })
    captcha = CaptchaField()

    #单次验证name字段是否已被注册
    def clean_name(self):
        name=self.cleaned_data.get('name')
        if User.objects.filter(name=name).exists():
            raise forms.ValidationError("该昵称已被使用")
        else:
            return name

    #全局验证，两次密码是否相同
    def clean(self):
        password=self.cleaned_data.get('password','password')
        re_password=self.cleaned_data.get('re_password','re_password')
        if password!=re_password:#验证两次密码是否相同
            raise forms.ValidationError({"re_password":"两次密码不一样"})
        return self.cleaned_data
