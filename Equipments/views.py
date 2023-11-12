from django.shortcuts import render
from django.shortcuts import get_object_or_404

from Equipments.serializers import EquipmentSerializer
from Equipments.models import Equipment

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class InventoryAPIView(APIView):
    # 기자재 상세정보 조회 API
    def get(self, request, pk):
        try:
            equip = Equipment.objects.get(pk=pk)
            serializer = EquipmentSerializer(equip)

            return Response(serializer.data)
        except Equipment.DoesNotExist:
            failMessage = {
                "message": "해당 기자재의 정보가 존재하지 않습니다."
            }
            return Response(failMessage, status =status.HTTP_404_NOT_FOUND)
