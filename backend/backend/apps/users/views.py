from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializers
from .models import UsersModel
from backend.utils import create_jwt


class UsersViews(APIView):
    """
    用户视图
    """
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        data = request.data
        try:
            serializer = UserSerializers(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            return Response({"msg": e.detail.__str__()}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data, 'msg': '添加用户成功'}, status=status.HTTP_201_CREATED)


class UsersLoginView(APIView):
    """
    用户登陆视图
    """
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        user = None
        data = request.data
        method = data.get("method")

        if method == 1:
            username = data.get("username", "")
            password = data.get("password", "")

            try:
                user = UsersModel.objects.get(username=username)
            except UsersModel.DoesNotExist:
                return Response({"msg": "用户名或密码错误"}, status=status.HTTP_400_BAD_REQUEST)

            if not user.check_password(password):
                return Response({"msg": "用户或密码错误"}, status=status.HTTP_400_BAD_REQUEST)

        if method == 2:
            mobile = data.get("mobile", "")
            code = data.get("code", "")
            try:
                user = UsersModel.objects.get(mobile=mobile)
            except UsersModel.DoesNotExist:
                return Response({"msg": "未绑定的手机号"}, status=status.HTTP_400_BAD_REQUEST)

            # 校验短信验证码
            redis_conn = get_redis_connection("default")
            real_sms_code = redis_conn.get('sms_%s' % mobile)
            redis_conn.delete('sms_%s' % mobile)

            if not real_sms_code or code != real_sms_code.decode():
                return Response({"msg": "验证码错误或已过期"}, status=status.HTTP_400_BAD_REQUEST)

        if user:
            res = {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "token": create_jwt(user)
            }

            return Response(res, status=status.HTTP_200_OK)






