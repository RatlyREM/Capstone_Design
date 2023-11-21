import jwt

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404

from Equipments.serializers import EquipmentSerializer
from Equipments.models import Equipment

from Accounts.utils import login_check

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class InventoryAPIView(APIView):
    #기자재 추가 API
    @login_check
    def post(self, request):
        try:
            if (request.user.is_staff):
                # 기자재 중복체크 필요
                get_object_or_404(Equipment, pk=request.data['model_name'])

                return Response({"message": "중복된 기자재를 입력했습니다."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "기자재를 추가할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except Http404:
            equipment = request.data
            serializer = EquipmentSerializer(data=equipment)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"message": "다시 로그인해 주십시오."}, status= status.HTTP_400_BAD_REQUEST)


class InventoryDetailAPIView(APIView):
    # 기자재 상세정보 조회 API
    def get(self, request, pk):
        try:
            equip = Equipment.objects.get(pk=pk)
            serializer = EquipmentSerializer(equip)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Equipment.DoesNotExist:
            failMessage = {
                "message": "해당 기자재의 정보가 존재하지 않습니다."
            }
            return Response(failMessage, status=status.HTTP_404_NOT_FOUND)
