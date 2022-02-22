"""
@Project ：QMS 
@File ：urls.py
@Author ：张建
@Date ：2022/2/17 10:56 下午 
"""

from django.urls import path
from .views import *

urlpatterns = [
    path("users/register/", UsersViews.as_view()),
    path("users/login/", UsersLoginView.as_view())
]