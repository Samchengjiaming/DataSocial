# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


#图形验证码模型
class CaptchaCaptchastore(models.Model):
    challenge = models.CharField(max_length=32)
    response = models.CharField(max_length=32)
    hashkey = models.CharField(unique=True, max_length=40)
    expiration = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'captcha_captchastore'

#用户模型
class User(models.Model):
    name = models.CharField(unique=True, max_length=15, blank=True, null=True)
    telephone = models.CharField(unique=True, max_length=11, blank=True, null=True)
    email = models.CharField(unique=True, max_length=25, blank=True, null=True)
    password = models.CharField(max_length=15, blank=True, null=True)
    register_date = models.DateField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'user'
