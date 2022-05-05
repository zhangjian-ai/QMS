"""
@Project ：QMS 
@File ：middleware.py
@Author ：Seeker
@Date ：2022/3/19 2:46 下午 
"""
import json

from django.utils.deprecation import MiddlewareMixin


class FormatBooleanMiddleware(MiddlewareMixin):
    """
    处理响应中的布尔值。True：1；False：0
    """

    def process_template_response(self, request, response):
        if hasattr(response, 'data'):
            data_str = json.dumps(response.data)
            data_str = data_str.replace("true", "1")
            data_str = data_str.replace("false", "0")
            response.data = json.loads(data_str)

        return response
