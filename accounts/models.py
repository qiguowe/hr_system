from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('用户必须有邮箱地址')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', User.SYSTEM_ADMIN)
        
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    """自定义用户模型，包含三种权限类型"""
    # 用户类型选项
    SYSTEM_ADMIN = 'system_admin'  # 系统管理员
    ADMIN = 'admin'  # 普通管理员
    NORMAL_USER = 'normal_user'  # 普通用户
    
    USER_TYPE_CHOICES = [
        (SYSTEM_ADMIN, '系统管理员'),
        (ADMIN, '普通管理员'),
        (NORMAL_USER, '普通用户'),
    ]
    
    email = models.EmailField(unique=True, verbose_name='邮箱')
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES, 
        default=NORMAL_USER,
        verbose_name='用户类型'
    )
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='电话')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    @property
    def is_system_admin(self):
        return self.user_type == self.SYSTEM_ADMIN
    
    @property
    def is_admin(self):
        return self.user_type == self.ADMIN
    
    @property
    def is_normal_user(self):
        return self.user_type == self.NORMAL_USER
