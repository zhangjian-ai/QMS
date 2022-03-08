import re

from django_redis import get_redis_connection
from rest_framework import serializers

from .models import UsersModel


class UserSerializers(serializers.ModelSerializer):
    """
    用户基本信息序列化器
    """
    confirm_password = serializers.CharField(label="确认密码", allow_null=False, write_only=True)
    sms_code = serializers.CharField(label="短信验证码", allow_null=False, write_only=True)

    class Meta:
        model = UsersModel
        fields = ['id', 'username', 'nickname', 'password', 'confirm_password', 'role', 'rank', 'sms_code', 'mobile']

        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 24,
            }
        }

    def validate(self, attrs):
        """
        用户创建时，字段校验
        """

        # 手机号校验
        mobile = attrs.get("mobile")

        if not re.match(r"^1[3-9]\d{9}$", mobile):
            raise serializers.ValidationError("手机号非法")

        try:
            UsersModel.objects.get(mobile=mobile)
        except UsersModel.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError("手机号已被注册")

        # 用户名校验
        try:
            UsersModel.objects.get(username=attrs.get("username"))
        except UsersModel.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError("用户名已存在")

        # 两次输入的密码校验
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("两次输入的密码不一致")

        # 校验短信验证码
        redis_conn = get_redis_connection("default")
        real_sms_code = redis_conn.get('sms_%s' % mobile).decode()

        if not real_sms_code:
            raise serializers.ValidationError("验证码已过期，请重新发送")

        if real_sms_code != attrs.get("sms_code"):
            raise serializers.ValidationError("验证码错误")

        return attrs

    def create(self, validated_data):
        """
        创建新用户
        """
        del validated_data["confirm_password"]
        del validated_data["sms_code"]

        # 取出密码，后面加密保存
        password = validated_data["password"]

        # 创建用户
        user = UsersModel(**validated_data)

        # 设置密码
        user.set_password(password)
        user.save()

        return user
