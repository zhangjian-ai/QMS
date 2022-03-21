from django.contrib import admin

from .models import *


# 注册到后台管理系统
@admin.register(UsersModel)
class UsersModelAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'nickname', 'mobile', 'username', 'role', 'rank']

    # 收索框查找的字段。外键需要指明匹配外键对象的具体字段
    search_fields = ['nickname', 'groups__name']

    # 多对多选项的默认样式及其难用，更好的方法是使用filter_horizontal或filter_vertical选项
    filter_horizontal = ['groups', 'user_permissions']


# 修改网站标题
admin.site.site_title = "QMS 后台"
admin.site.site_header = "QMS"
