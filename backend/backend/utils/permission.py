"""
@Project ：QMS 
@File ：permission.py
@Author ：张建
@Date ：2022/3/21 10:47 上午
@Desc ：自定义权限统一采用权限组的方式分配控制，命名方式：服务名_操作1_操作2(均大写)，例如：SERVICE_CREATE_UPDATE_DELETE
"""
from rest_framework import permissions
from django.contrib.auth.models import Group

from users.models import UsersModel


class ServicePermission(permissions.BasePermission):
    """
    has_object_permission方法在has_permission方法返回值True之后调用，除了在POST方法中（在POST方法中仅执行has_permission）。
    当从permission_classes方法返回False值时，请求不会获得任何权限，也不会循环更多，否则，它会检查循环的所有权限。
    has_permission方法将对所有请求调用（GET，POST，PUT，DELETE）HTTP。
    has_object_permission方法不会对HTTP POST请求调用，因此对POST的校验在 has_permission 方法中完成。
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            user = request.user
            group = Group.objects.get(name='SERVICE_CREATE_UPDATE_DELETE')
            # 如果用户和组有关联关系，则说明有权限
            UsersModel.objects.get(id=user.id, groups=group)
        except Group.DoesNotExist:
            pass
        except UsersModel.DoesNotExist:
            return False

        return True





