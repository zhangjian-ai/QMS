from django.db import models
from django.contrib.auth.models import AbstractUser


class UsersModel(AbstractUser):
    """
    用户基本信息模型
    """

    nickname = models.CharField(max_length=36, null=False, verbose_name="昵称")
    mobile = models.CharField(max_length=11, null=False, unique=True, verbose_name="手机号")

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname