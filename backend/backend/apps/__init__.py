from django.db import models
from django.utils import timezone


class CustomDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        """重写该方法，格式化时间格式后再保存到数据库"""
        val = super().pre_save(model_instance, add)
        val = timezone.datetime.strftime(val, "%Y-%m-%d %H:%M:%S")

        return val


class BaseModel(models.Model):
    create_time = CustomDateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = CustomDateTimeField(auto_now=True, verbose_name="最近修改时间")

    class Meta:
        abstract = True
