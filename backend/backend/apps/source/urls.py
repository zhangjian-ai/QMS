"""
@Project ：QMS 
@File ：urls.py
@Author ：Seeker
@Date ：2022/3/8 8:38 下午 
"""

from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('source/staff', StaffView.as_view()),
    path('source/sysInfo', SystemView.as_view()),
    path('source/proto', ProtocolView.as_view()),
    path('source/menu', MenuView.as_view()),
]