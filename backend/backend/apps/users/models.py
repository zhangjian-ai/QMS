from django.db import models
from django.contrib.auth.models import AbstractUser

from backend.utils import STAFF_ROLE, STAFF_RANK, TEST_ROLE


class UsersModel(AbstractUser):
    """
    用户基本信息模型
    """

    nickname = models.CharField(max_length=36, null=False, verbose_name="昵称")
    mobile = models.CharField(max_length=11, null=False, unique=True, verbose_name="手机号")
    role = models.SmallIntegerField(choices=STAFF_ROLE, null=False, default=0, verbose_name="职位")
    rank = models.SmallIntegerField(choices=STAFF_RANK, null=False, default=0, verbose_name="职级")

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


class TestRoleModel(models.Model):
    """
    测试角色模型
    """

    id = models.SmallIntegerField(verbose_name="ID", primary_key=True, auto_created=True)
    name = models.SmallIntegerField(choices=TEST_ROLE, unique=True, default=0, verbose_name="测试角色")
    username = models.CharField(max_length=50, null=False, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=50, null=False, unique=True, verbose_name="密码")
    user = models.OneToOneField(UsersModel, verbose_name="系统用户", related_name="test_role",
                                null=False, on_delete=models.RESTRICT)

    class Meta:
        db_table = "test_role"
        verbose_name = "测试角色账户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
