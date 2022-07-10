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
            return Response({'msg': "无效的服务ID"}, status=status.HTTP_400_BAD_REQUEST)
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


class ServiceListView(APIView):
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


class LatestUseServiceView(APIView):
    """
    最近使用服务视图
    """

    def get(self, request):
        """
        获取登录用户最近一次使用的服务
        首次获取时使用一个默认服务新建记录
        :param request:
        :return:
        """

        user = request.user

        try:
            query = LatestUseServiceModel.objects.get(user_id=user.id)
        except LatestUseServiceModel.DoesNotExist:
            # 如果当前无记录就新建一条
            service = ServiceModel.objects.filter(flag=True)

            try:
                service_dict = ServiceSerializer(instance=service[0]).data
            except IndexError:
                return Response({'msg': "当前无可用服务", 'id': None, 'service': None})

            LatestUseServiceModel.objects.create(user_id=user, service_id=service[0])
        else:
            service_dict = ServiceSerializer(instance=query.service_id).data

        return Response({'id': service_dict['id'], 'name': service_dict['name']})

    def put(self, request):
        """
        变更用户最近使用服务记录
        :param request:
        :return:
        """

        user = request.user
        service_id = request.data.pop('service_id', None)

        if not service_id:
            return Response({'msg': '无效表单'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            query = LatestUseServiceModel.objects.get(user_id=user.id)
        except LatestUseServiceModel.DoesNotExist:
            # 如果当前无记录就新建一条
            try:
                service = ServiceModel.objects.get(id=service_id)
                if not service.flag:
                    return Response({'msg': "该服务已被禁用"}, status=status.HTTP_400_BAD_REQUEST)
            except ServiceModel.DoesNotExist:
                return Response({'msg': "无效的service_id"}, status=status.HTTP_400_BAD_REQUEST)

            LatestUseServiceModel.objects.create(user_id=user, service_id=service)
            service_dict = ServiceSerializer(instance=service)
        else:
            service_dict = ServiceSerializer(instance=query.service_id)

        return Response({'id': service_dict['id'], 'name': service_dict['name']})


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
            return Response({'msg': "无效的模块ID"}, status=status.HTTP_400_BAD_REQUEST)
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


class ModuleListView(APIView):
    """
    查询所有模块列表
    """

    def get(self, request):
        """
        默认只获取可用的模块
        :param request:
        :return:
        """

        query_set = ModuleModel.objects.filter(flag=True)
        serializer = ModuleSerializer(instance=query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InterfaceView(APIView):
    """
    接口视图
    """

    def get(self, request):
        """
        查询接口
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

        if data.get('uri', None):
            cls_name = data.pop('uri')
            query_set = InterfaceModel.objects.filter(**data, uri__contains=cls_name)
        else:
            query_set = InterfaceModel.objects.filter(**data)

        total = query_set.count()
        serializer = InterfaceSerializer(instance=query_set[(page - 1) * size: page * size], many=True)
        return Response({'total': total, 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        创建接口
        :param request:
        :return:
        """

        data = request.data

        try:
            serializer = InterfaceSerializer(data=data, context={"user": request.user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            return Response({"msg": e.detail.__str__()}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data, 'msg': '创建接口成功'}, status=status.HTTP_201_CREATED)

    def put(self, request):
        """
        更新模块
        :param request:
        :return:
        """
        data = request.data
        interface_id = data.pop('id')

        try:
            interface = InterfaceModel.objects.get(id=interface_id)

            serializer = InterfaceSerializer(instance=interface, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except InterfaceModel.DoesNotExist:
            return Response({'msg': "无效的接口ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"msg": e.detail.__str__()}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data, 'msg': '更新接口成功'}, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        删除服务
        :param request:
        :return:
        """
        interface_id = request.data.get("id")

        if not interface_id:
            return Response({'msg': '无效的接口ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            interface = InterfaceModel.objects.get(id=interface_id)
        except ModuleModel.DoesNotExist:
            return Response({'msg': "无效的接口ID"}, status=status.HTTP_400_BAD_REQUEST)

        interface.delete()

        return Response({'msg': '接口已删除'}, status=status.HTTP_200_OK)
