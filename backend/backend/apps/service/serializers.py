"""
@Project ：QMS 
@File ：serializers.py
@Author ：张建
@Date ：2022/3/15 4:38 下午 
"""
from rest_framework import serializers

from .models import ServiceModel
from backend.utils import BaseModelSerializer


class ServiceSerializer(BaseModelSerializer):
    """
    服务序列化器
    """

    protocol_str = serializers.CharField(source='get_protocol_display', read_only=True)

    class Meta:
        model = ServiceModel
        fields = '__all__'
        read_only_fields = ('id', )
