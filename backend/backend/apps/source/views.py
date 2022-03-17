from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.utils import STAFF_ROLE, STAFF_RANK, NAME, CULTURE, API_PROTO


class StaffView(APIView):
    """
    职员配置信息
    """

    def get(self, request):
        return Response({
            "role": STAFF_ROLE,
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


class ProtocolView(APIView):
    """
    系统协议
    """
    def get(self, request):
        return Response(API_PROTO, status=status.HTTP_200_OK)
