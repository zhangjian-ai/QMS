"""
@Project ：QMS 
@File ：serializers.py
@Author ：Seeker
@Date ：2022/3/15 4:38 下午 
"""
from rest_framework import serializers

from .models import *
from backend.utils import BaseModelSerializer


class ServiceSerializer(BaseModelSerializer):
    """
    服务序列化器
    """

    protocol_str = serializers.CharField(source='get_protocol_display', read_only=True)

    class Meta:
        model = ServiceModel
        fields = '__all__'
        read_only_fields = ('id',)


class ModuleSerializer(BaseModelSerializer):
    """
    模块序列化器
    """

    creator_name = serializers.CharField(source='creator', read_only=True, label='创建人')
    service_name = serializers.CharField(source='service', read_only=True, label='归属服务')

    class Meta:
        model = ModuleModel
        fields = '__all__'
        read_only_fields = ('id', 'creator', )

    def create(self, validated_data):
        """
        为模块创建时，添加创建人
        :param validated_data:
        :return:
        """
        user = self.context.get("user")
        validated_data['creator'] = user

        return super(ModuleSerializer, self).create(validated_data)


class InterfaceSerializer(BaseModelSerializer):
    """
    接口序列化器
    """

    creator_name = serializers.CharField(source='creator', read_only=True, label='创建人')
    module_name = serializers.CharField(source='module', read_only=True, label='归属模块')

    class Meta:
        model = InterfaceModel
        fields = '__all__'
        read_only_fields = ('id', 'creator', )

    def create(self, validated_data):
        """
        为接口创建时，添加创建人
        :param validated_data:
        :return:
        """
        user = self.context.get("user")
        validated_data['creator'] = user

        return super(InterfaceSerializer, self).create(validated_data)
