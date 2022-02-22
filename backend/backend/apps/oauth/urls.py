"""
@Project ：QMS 
@File ：urls.py
@Author ：张建
@Date ：2022/2/17 10:43 下午 
"""

from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path('oauth/smsCode/(?P<mobile>1[3-9]\d{9})/', SmsCodeView.as_view()),
]
