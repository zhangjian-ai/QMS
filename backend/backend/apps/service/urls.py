"""
@Project ：QMS 
@File ：urls.py
@Author ：张建
@Date ：2022/3/15 5:53 下午 
"""

from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('service', ServiceView.as_view()),
    path('allService', AllServiceView.as_view()),
    path('module', ModuleView.as_view()),
]
