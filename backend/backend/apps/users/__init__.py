import os

from django.apps import AppConfig

# 更改默认的配置路径
default_app_config = 'users.UsersConfig'


# 重写类FilesConfig，这个类配合上面的路径使用
class UsersConfig(AppConfig):
    name = os.path.split(os.path.dirname(__file__))[-1]
    verbose_name = "成员管理"
