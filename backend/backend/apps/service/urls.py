"""
@Project ：QMS 
@File ：urls.py
@Author ：Seeker
@Date ：2022/3/15 5:53 下午 
"""

from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('service', ServiceView.as_view()),
    path('allService', ServiceListView.as_view()),
    path('lus', LatestUseServiceView.as_view()),
    path('module', ModuleView.as_view()),
    path('allModule', ModuleListView.as_view()),
    path('interface', InterfaceView.as_view())
]
