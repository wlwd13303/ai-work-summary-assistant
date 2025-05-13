from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    '''自定义用户管理器'''

    def create_user(self, email, username, password, **extra_fields):
        '''创建普通用户'''
        if not email:
            raise ValueError('用户必须有邮箱地址')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        '''创建超级用户'''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置 is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置 is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    '''自定义用户模型'''
    email = models.EmailField(_('邮箱地址'), unique=True)
    username = models.CharField(_("用户名"), max_length=150, unique=True)

    USERNAME_FIELD = 'email'  # 使用邮箱作为登录凭证
    REQUIRED_FIELDS = ['username']  # 创建超级用户时需要的字段

    objects = UserManager()

    def __str__(self):
        return self.username
