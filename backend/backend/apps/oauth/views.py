import random

from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.utils.constants import SMS_CODE_EXPIRES, SMS_CODE_INTERVAL


class SmsCodeView(APIView):
    """
    验证码视图
    """
    permission_classes = []
    authentication_classes = []

    def get(self, request, mobile):
        # 获取redis链接
        redis = get_redis_connection("default")

        # 检查当前手机号是否已经发送过验证码
        if redis.get("sms_flag_%s" % mobile):
            return Response({"msg": "验证码发送过于频繁"}, status.HTTP_400_BAD_REQUEST)

        # 生成随机验证码
        sms_code = str(random.randint(0, 999999)).zfill(6)

        # 创建redis管道对象
        pipe = redis.pipeline()
        pipe.setex("sms_%s" % mobile, SMS_CODE_EXPIRES, sms_code)
        pipe.setex("sms_flag_%s" % mobile, SMS_CODE_INTERVAL, 1)
        pipe.execute()

        return Response({
            "msg": "验证码已发送，五分钟内有效",
            "code": sms_code
        }, status.HTTP_200_OK)
