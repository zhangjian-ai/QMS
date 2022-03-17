from django.db import models

from backend.utils import BaseModel, API_PROTO

from users.models import UsersModel, TestRoleModel


class ServiceModel(BaseModel):
    """
    系统服务模型
    """

    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=30, verbose_name="服务名称", null=False, unique=True)
    domain = models.CharField(max_length=100, verbose_name="域名", null=False)
    port = models.SmallIntegerField(verbose_name="端口号", null=True)
    protocol = models.SmallIntegerField(choices=API_PROTO, verbose_name="协议", default=0)
    flag = models.BooleanField(verbose_name="可用", null=False, default=True)

    class Meta:
        db_table = "service"
        verbose_name = "系统服务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ModuleModel(BaseModel):
    """
    系统模块模型
    """

    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=30, verbose_name="模块名称", null=False, unique=True)
    cls_name = models.CharField(max_length=50, verbose_name="自动化类名", null=False, db_index=True)
    flag = models.BooleanField(verbose_name="可用", null=False, default=True)
    service = models.ForeignKey(ServiceModel, verbose_name="服务", related_name="module", on_delete=models.RESTRICT,
                                null=False)
    creator = models.ForeignKey(UsersModel, verbose_name="创建人", related_name="module", on_delete=models.RESTRICT,
                                null=False)

    class Meta:
        db_table = "module"
        verbose_name = "系统模块"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class InterfaceModel(BaseModel):
    """
    接口模型
    """

    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=30, verbose_name="接口名称", null=False, db_index=True, unique=True)
    uri = models.CharField(max_length=50, verbose_name="接口URI", null=False)
    flag = models.BooleanField(verbose_name="可用", null=False, default=True)
    module = models.ForeignKey(ModuleModel, verbose_name="模块", related_name="interface", on_delete=models.RESTRICT,
                               null=False)
    creator = models.ForeignKey(UsersModel, verbose_name="创建人", related_name="interface", on_delete=models.RESTRICT,
                                null=False)

    class Meta:
        db_table = "interface"
        verbose_name = "模块接口"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class InterfaceDataModel(BaseModel):
    """
    接口数据包模型
    """

    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=50, verbose_name="数据包名", null=False, db_index=True, unique=True)
    test_role = models.ForeignKey(TestRoleModel, verbose_name="测试角色", related_name="interface_data",
                                  on_delete=models.RESTRICT, null=False)
    interface = models.ForeignKey(InterfaceModel, verbose_name="接口", related_name="interface_data",
                                  on_delete=models.RESTRICT, null=False)
    pre_interface_data = models.ForeignKey('self', verbose_name="前置数据包", related_name="pre",
                                           on_delete=models.RESTRICT, null=False)

    class Meta:
        db_table = "interface_data"
        verbose_name = "接口数据包"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class InterfaceDataDetailModel(BaseModel):
    """
    接口数据包详情模型
    """

    id = models.AutoField(verbose_name="ID", primary_key=True)
    request = models.JSONField(verbose_name="请求数据")
    response = models.JSONField(verbose_name="期望响应数据")
    interface_data = models.OneToOneField(InterfaceDataModel, verbose_name="数据包", related_name="detail",
                                          on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "interface_data_detail"
        verbose_name = "接口数据包详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.interface_data.__str__()
