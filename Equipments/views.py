from django.shortcuts import render
from django.shortcuts import get_object_or_404,get_list_or_404

from django.http import Http404
from operator import attrgetter

from Equipments.serializers import EquipmentSerializer, LogSerializer
from Equipments.models import Equipment,Log

from Accounts.utils import login_check

from Bookmark.models import Favorites

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

class LogAPIView(APIView):
    #입출고 현황 조회 API
    def get(self, request):
        log_objects = Log.objects.all().order_by('-updated_at')

        if not log_objects.exists():
            return Response({"message": "로그 데이터가 없습니다."}, status= status.HTTP_204_NO_CONTENT)

        serializer = LogSerializer(log_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookmarkLogAPIView(APIView):
    #현재 로그인한 유저가 즐겨찾기 해둔 기자재의 로그 내역만 조회
    @login_check
    def get(self, request):
        try:
            # 로그인한 유저의 즐겨찾기 기자재를 모두 가져온다.
            fav = Favorites.objects.filter(user_id=request.user.id)

            log_list = []

            # 즐겨찾기 기자재의 로그들만 가져온다.
            for i in fav:
                bookmark_name = i.model_name.model_name
                logs = Log.objects.filter(model_name=bookmark_name)
                log_list.extend(logs)

            if len(log_list) == 0 or len(fav) == 0:
                raise ValidationError
            log_list = sorted(log_list, key=attrgetter('updated_at'), reverse=True)

            serializer = LogSerializer(log_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({"message": "해당 유저의 즐겨찾기 기자재 로그가 존재하지 않습니다."}, status= status.HTTP_404_NOT_FOUND)

class InventoryAPIView(APIView):
    #전체 기자재 리스트 표시(이름순)
    def get(self, request):
        equip = Equipment.objects.all().order_by('model_name')

        if not equip.exists():
            return Response({"message": "기자재 데이터가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        serializer = EquipmentSerializer(equip, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #기자재 정보 추가 API
    @login_check
    def post(self, request):
        try:
            if request.user.is_staff:
                # 기자재 중복체크 필요
                get_object_or_404(Equipment, pk=request.data['model_name'])

                return Response({"message": "중복된 기자재를 입력했습니다."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "기자재를 추가할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except Http404:
            equipment = request.data
            serializer = EquipmentSerializer(data=equipment)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"message": "model_name을 올바르게 전달하세요."}, status=status.HTTP_400_BAD_REQUEST)


    #기자재 정보 수정 API
    @login_check
    def put(self, request):
        try:
            if request.user.is_staff:
                equip = Equipment.objects.get(pk =request.data['model_name'])

                serializer = EquipmentSerializer(equip, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "기자재를 수정할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except Equipment.DoesNotExist:
            return Response({"message": "해당 기자재의 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"message": "model_name을 올바르게 전달하세요."}, status=status.HTTP_400_BAD_REQUEST)


class InventoryDetailAPIView(APIView):
    # 기자재 정보 조회 API
    def get(self, request, pk):
        try:
            equip = Equipment.objects.get(pk=pk)
            serializer = EquipmentSerializer(equip)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Equipment.DoesNotExist:
            return Response({"message": "해당 기자재의 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

    #기자재 정보 삭제 API
    @login_check
    def delete(self, request, pk):
        try:
            if request.user.is_staff:
                equip = get_object_or_404(Equipment, pk= pk)

                # 삭제 진행
                equip.delete()
                return Response({"message": "삭제 성공"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "기자재를 삭제할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except Http404:
            return Response({"message": "삭제할 기자재를 찾지 못했습니다."}, status=status.HTTP_404_NOT_FOUND)

class InventoryInqTotalRentAPIView(APIView):
    #기자재 정보 조회 API(총 조회수 많은 순서)
    def get(self, request):
        equip = Equipment.objects.all().order_by('-total_rent')

        if not equip.exists():
            return Response({"message": "기자재 데이터가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        serializer = EquipmentSerializer(equip, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InventoryInqUpdatedAtAPIView(APIView):
    #기자재 정보 조회 API(기자재 정보 추가된 시간 순서)
    def get(self, request):
        equip = Equipment.objects.all().order_by('-updated_at')

        if not equip.exists():
            return Response({"message": "기자재 데이터가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        serializer = EquipmentSerializer(equip, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InventorySearchAPIView(APIView):
    #기자재 검색 API (model_name,name,type,repository,manufacturer)
     def post(self, request):
         try:
            if not request.data['searchData']:
                equip = Equipment.objects.all()
                serializer = EquipmentSerializer(equip, many=True)
                return Response(serializer.data, status= status.HTTP_200_OK)

            search = request.data['searchData']
            modelnameResult = list(Equipment.objects.filter(model_name__icontains= search))
            nameResult = list(Equipment.objects.filter(name__icontains = search))
            typeResult = list(Equipment.objects.filter(type__icontains=search))
            repositoryResult = list(Equipment.objects.filter(repository__icontains=search))
            manufacturerResult = list(Equipment.objects.filter(manufacturer__icontains=search))

            combined_object = modelnameResult+nameResult+typeResult+repositoryResult+manufacturerResult
            combined_object = sorted(combined_object,key=attrgetter('model_name'))

            if len(combined_object) == 0:
                raise ValidationError
            serializer = EquipmentSerializer(combined_object, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

         except ValidationError:
             return Response({"message": "검색 결과가 없습니다."}, status= status.HTTP_204_NO_CONTENT)
         except KeyError:
             return Response({"message": "공백으로라도 searchData 전달 필요"}, status= status.HTTP_400_BAD_REQUEST)




