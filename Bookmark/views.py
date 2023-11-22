from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404

from django.http import Http404
from operator import attrgetter

from Equipments.models import Equipment

from Bookmark.serializers import FavoritesSerializer
from Bookmark.models import Favorites

from Accounts.utils import login_check

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

class FavoritesAPIView(APIView):
    #내 즐겨찾기 목록에 추가 API
    @login_check
    def post(self, request):
        try:
            #해당 기자재 정보가 있는지 확인
            Equipment.objects.get(pk= request.data['model_name'])

            request.data['user_id'] = request.user.id

            #즐겨찾기 목록에서 중복 체크
            get_object_or_404(Favorites, user_id = request.user.id, model_name=request.data['model_name'])

            return Response({"message": "이미 즐겨찾기 목록에 존재합니다."}, status= status.HTTP_400_BAD_REQUEST)
        except Equipment.DoesNotExist:
            return Response({"message": "해당 기자재의 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Http404:
            serializer = FavoritesSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"message": "model_name을 올바르게 전달하세요."}, status=status.HTTP_400_BAD_REQUEST)

    #내 즐겨찾기 목록 조회 API
    @login_check
    def get(self, request):
        try:
            fav = get_list_or_404(Favorites, user_id=request.user.id)
            fav = sorted(fav, key=lambda x: x.model_name.model_name)

            if len(fav) == 0:
                raise ValidationError
            serializer = FavoritesSerializer(fav, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({"message": "해당 유저의 즐겨찾기 목록이 없습니다."}, status= status.HTTP_404_NOT_FOUND)

class FavoritesDeleteAPIView(APIView):
    # @login_check
    # def get(self,request, pk):
    #     try:
    #         fav = get_object_or_404(Favorites, user_id=request.user.id, model_name=pk)
    #         serializer = FavoritesSerializer(fav)
    #         return Response(serializer.data, status= status.HTTP_200_OK)
    #     except Http404:
    #         return Response({"message": "해당 기자재가 즐겨찾기 리스트에 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    # 내 즐겨찾기 기자재 삭제 API
    @login_check
    def delete(self, request,pk):
        try:
            fav = get_object_or_404(Favorites, user_id=request.user.id, model_name=pk)

            # 삭제 진행
            fav.delete()
            return Response({"message": "삭제 성공"}, status=status.HTTP_204_NO_CONTENT)

        except Http404:
            return Response({"message": "해당 기자재가 즐겨찾기 리스트에 없습니다."}, status=status.HTTP_404_NOT_FOUND)

