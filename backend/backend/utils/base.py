"""
@Project ：QMS 
@File ：base.py
@Author ：Seeker
@Date ：2022/3/13 10:10 下午 
"""

from django.db import models
from django.utils import timezone
from rest_framework.fields import DateTimeField
from rest_framework.serializers import ModelSerializer


class ModelDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        """重写该方法，在保存之前完成时间格式化"""
        val = super().pre_save(model_instance, add)
        val = timezone.datetime.strftime(val, '%Y-%m-%d %H:%M:%S')

        return val


class BaseModel(models.Model):
    """模型基类"""

    create_time = ModelDateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = ModelDateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True


class SerializerDateTimeField(DateTimeField):
    def to_representation(self, value):
        """重写该方法，统一配置序列化时间的格式"""

        self.format = '%Y-%m-%d %H:%M:%S'
        val = super().to_representation(value)

        return val


class BaseModelSerializer(ModelSerializer):
    """模型序列化器基类"""

    serializer_field_mapping = ModelSerializer.serializer_field_mapping
    serializer_field_mapping[models.DateTimeField] = SerializerDateTimeField
