from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_TYPE = (
        ('M', '男'),
        ('F', '女')
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        '用户名',
        max_length=150,
        unique=True,
        help_text='用户名，不超过150个字符。仅可包含英文字母、数字以及@/./+/-/_',
        validators=[username_validator],
        error_messages={
            'unique': '该用户名已存在。'
        },
    )
    nickname = models.CharField('昵称', max_length=32)
    gender = models.CharField('性别', max_length=2, choices=GENDER_TYPE, default='M')
    email = models.EmailField('邮箱地址', max_length=150, blank=True, null=True)
    phone = models.CharField('手机号', max_length=11, blank=True, null=True)
    is_staff = models.BooleanField(verbose_name='管理人员权限', default=False)
    date_joined = models.DateTimeField('注册时间', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'gender']

    class Meta:
        verbose_name = '用户'

    def __str__(self):
        return self.username
