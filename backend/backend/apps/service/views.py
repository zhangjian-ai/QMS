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

        try:
            serializer = ServiceSerializer(data=data)
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
        service_id = data.pop("id", None)

        try:
            service = ServiceModel.objects.get(id=service_id)

            serializer = ServiceSerializer(data=data, instance=service, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ServiceModel.DoesNotExist:
            return Response({'msg': "无法更新不存在的服务"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"msg": e.detail.__str__()}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data, 'msg': '更新服务成功'}, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        删除服务
        :param request:
        :return:
        """
        service_id = request.data.get("id")

        if not service_id:
            return Response({'msg': '无效的服务ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service = ServiceModel.objects.get(id=service_id)
        except ServiceModel.DoesNotExist:
            return Response({'msg': "无效的服务ID"}, status=status.HTTP_400_BAD_REQUEST)

        service.delete()

        return Response({'msg': '服务已删除'}, status=status.HTTP_200_OK)


class AllServiceView(APIView):
    """
    查询所有服务列表
    """

    def get(self, request):
        """
        默认只获取可用的服务
        :param request:
        :return:
        """

        query_set = ServiceModel.objects.filter(flag=True)
        serializer = ServiceSerializer(instance=query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ModuleView(APIView):
    """
    模块视图
    """

    def get(self, request):
        """
        查询模块
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

        if data.get('cls_name', None):
            cls_name = data.pop('cls_name')
            query_set = ModuleModel.objects.filter(**data, cls_name__contains=cls_name)
        else:
            query_set = ModuleModel.objects.filter(**data)

        total = query_set.count()
        serializer = ModuleSerializer(instance=query_set[(page - 1) * size: page * size], many=True)
        return Response({'total': total, 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        创建模块
        :param request:
        :return:
        """

        data = request.data

        try:
            serializer = ModuleSerializer(data=data, context={"user": request.user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            return Response({"msg": e.detail.__str__()}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data, 'msg': '新增模块成功'}, status=status.HTTP_201_CREATED)

    def put(self, request):
        """
        更新模块
        :param request:
        :return:
        """
        data = request.data
        module_id = data.pop('id')

        try:
            module = ModuleModel.objects.get(id=module_id)

            serializer = ModuleSerializer(instance=module, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ModuleModel.DoesNotExist:
            return Response({'msg': "无法更新不存在的模块"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"msg": e.detail.__str__()}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data, 'msg': '更新模块成功'}, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        删除服务
        :param request:
        :return:
        """
        module_id = request.data.get("id")

        if not module_id:
            return Response({'msg': '无效的模块ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            module = ModuleModel.objects.get(id=module_id)
        except ModuleModel.DoesNotExist:
            return Response({'msg': "无效的模块ID"}, status=status.HTTP_400_BAD_REQUEST)

        module.delete()

        return Response({'msg': '模块已删除'}, status=status.HTTP_200_OK)
