# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CaptchaCaptchastore(models.Model):
    challenge = models.CharField(max_length=32)
    response = models.CharField(max_length=32)
    hashkey = models.CharField(unique=True, max_length=40)
    expiration = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'captcha_captchastore'


class DatasetInfo(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    dataset_title = models.CharField(unique=True, max_length=100)
    data_sources = models.CharField(max_length=500, blank=True, null=True)
    dataset_up_day = models.DateField(blank=True, null=True)
    dataset_path = models.CharField(unique=True, max_length=50)
    dataset_img_path = models.CharField(max_length=200, blank=True, null=True)
    dataset_private = models.IntegerField()
    author_id = models.IntegerField(blank=True, null=True)
    favour = models.IntegerField(blank=True, null=True)
    recommend = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_info'


class DatasetInfoBackground(models.Model):
    dataset_info_background_id = models.IntegerField(primary_key=True)
    dataset_info_background_content = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'dataset_info_background'


class DatasetInfoIntroduce(models.Model):
    dataset_info_introduce_id = models.CharField(max_length=12)
    dataset_info_introduce_content = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'dataset_info_introduce'


class DatasetInfoLabels(models.Model):
    dataset_info_labels_id = models.IntegerField(primary_key=True)
    dataset_info_label_1 = models.CharField(max_length=20)
    dataset_info_label_2 = models.CharField(max_length=20)
    dataset_info_label_3 = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'dataset_info_labels'


class DatasetInfoProblem(models.Model):
    dataset_info_problem_id = models.CharField(max_length=12)
    dataset_info_problem_content = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'dataset_info_problem'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TaskInfo(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_title = models.CharField(unique=True, max_length=100)
    task_describe = models.CharField(max_length=200)
    task_require = models.CharField(max_length=200)
    author_id = models.IntegerField()
    coin = models.IntegerField()
    up_day = models.DateField()
    deadline = models.DateField()
    dataset_img_path = models.CharField(max_length=50, blank=True, null=True)
    dataset_path = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'task_info'


class User(models.Model):
    name = models.CharField(unique=True, max_length=15, blank=True, null=True)
    telephone = models.CharField(unique=True, max_length=11, blank=True, null=True)
    email = models.CharField(unique=True, max_length=25, blank=True, null=True)
    password = models.CharField(max_length=15, blank=True, null=True)
    register_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'user'


class UserCollectDatasetHub(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    collect_dataset_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_collect_dataset_hub'


class UserInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    school_or_company = models.CharField(max_length=200, blank=True, null=True)
    major_or_position = models.CharField(max_length=200, blank=True, null=True)
    place = models.CharField(max_length=200, blank=True, null=True)
    personal_web = models.CharField(max_length=500, blank=True, null=True)
    signature = models.CharField(max_length=100, blank=True, null=True)
    class_field = models.IntegerField(db_column='class', blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'user_info'
