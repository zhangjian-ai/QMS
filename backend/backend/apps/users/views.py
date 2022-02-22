from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializers
from .models import UsersModel
from backend.utils import create_jwt


class UsersViews(APIView):
    """
    用户信息视图
    """

    def post(self, request):
        data = request.data
        try:
            serializer = UserSerializers(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            return Response({"msg": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsersLoginView(APIView):
    """
    用户登陆视图
    """

    def post(self, request):
        data = request.data

        username = data.get("username", "")
        password = data.get("password", "")

        try:
            user = UsersModel.objects.get(username=username)
        except UsersModel.DoesNotExist:
            return Response({"msg": "用户或密码错误"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if user.check_password(password):
                res = {
                    "id": user.id,
                    "username": user.username,
                    "nickname": user.nickname,
                    "token": create_jwt(user)
                }
                return Response(res, status=status.HTTP_200_OK)
            return Response({"msg": "用户或密码错误"}, status=status.HTTP_400_BAD_REQUEST)
