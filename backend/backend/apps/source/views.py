from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.utils import ROLE, STAFF_RANK, NAME, CULTURE


class StaffView(APIView):
    """
    职员配置信息
    """

    def get(self, request):
        return Response({
            "role": ROLE,
            "rank": STAFF_RANK
        }, status=status.HTTP_200_OK)


class SystemView(APIView):
    """
    系统信息
    """

    def get(self, request):
        return Response({
            "name": NAME,
            "culture": CULTURE
        }, status=status.HTTP_200_OK)
