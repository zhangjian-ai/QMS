from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from backend.utils.permission import ServicePermission


class ServiceView(APIView):
    """
    服务视图
    """
    permission_classes = [ServicePermission, ]

    def get(self, request):
        """
        查询服务列表
        :param request:
        :return:
        """
        query_dict = request.query_params
        keys = query_dict.keys()
        data = {}

        for key in keys:
            if query_dict.get(key):
                data[key] = query_dict.get(key)

        page = int(data.pop('page', 1))
        size = int(data.pop('page_size', 10))

        if data.get('domain', None):
            domain = data.pop('domain')
            query_set = ServiceModel.objects.filter(**data, domain__contains=domain)
        else:
            query_set = ServiceModel.objects.filter(**data)

        total = query_set.count()
        serializer = ServiceSerializer(instance=query_set[(page - 1) * size: page * size], many=True)
        return Response({'total': total, 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        创建服务
        :param request:
        :return:
        """
        data = request.data
        serializer = ServiceSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            return Response({"msg": e.detail.__str__()}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data, 'msg': '新增服务成功'}, status=status.HTTP_201_CREATED)

    def put(self, request):
        """
        修改服务
        :param request:
        :return:
        """
        data = request.data
        id = data.pop("id", None)

        try:
            service = ServiceModel.objects.get(id=id)

            serializer = ServiceSerializer(data=data, instance=service, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ServiceModel.DoesNotExist:
            return Response({'msg': "无法更新不存在的服务"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"msg": e.detail.__str__()}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data, 'msg': '更新服务成功'}, status=status.HTTP_200_OK)
