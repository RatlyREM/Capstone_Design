from django.shortcuts import render
from django.shortcuts import get_object_or_404,get_list_or_404

from django.http import Http404
from operator import attrgetter

from Accounts.models import User
from Equipments.serializers import EquipmentSerializer, LogCreateSerializer, LogModifySerializer, RentSerializer,LogRentAcceptedSerializer,ReturnedSerializer,RequestGetRentingSerializer,RequestGetReturningSerializer
from Equipments.models import Equipment,Log,Renting, Returning, Returned
from django.utils import timezone

from Accounts.utils import login_check

from Bookmark.models import Favorites

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

class RequestGetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 7-2 승인 대기 중인 리스트 조회 API
    def get(self, request):
        try:
            if request.user.is_staff:
                rent_obj = Renting.objects.filter(rent_accepted_date__isnull= True)
                return_obj = Returning.objects.all()

                if len(rent_obj) == 0 and len(return_obj) == 0:
                    raise ValidationError

                rent_serializer = RequestGetRentingSerializer(rent_obj, many=True)
                return_serializer = RequestGetReturningSerializer(return_obj, many=True)


                r = {
                    "rent": rent_serializer.data,
                    "return": return_serializer.data,
                }

                return Response(r, status= status.HTTP_200_OK)
            else:
                return Response({"message": "승인 대기 리스트를 볼 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError:
            return Response({"message": "승인 대기중인 내역이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)


class ReturnedGetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 7-3 나의 반납 완료한 리스트 조회 API
    def get(self,request):
        #1년 계산 후 넘은 것은 삭제
        one_years_ago = timezone.now()- timezone.timedelta(days=365)

        old_objects = Returned.objects.filter(return_accepted_date__lt= one_years_ago)
        old_objects.delete()

        returned_obj = Returned.objects.filter(user_id=request.user.id).order_by('-return_accepted_date')

        if len(returned_obj) == 0:
            return Response({"message": "반납 완료한 데이터가 없습니다."}, status= status.HTTP_404_NOT_FOUND)

        serializer = ReturnedSerializer(returned_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RentRefusedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 7-10 대여 승인 거절 API
    def get(self, request, pk):
        try:
            log_obj = Log.objects.get(pk=pk)

            if request.user.is_staff:
                #대여 승인 가능한 상태인지 확인
                if log_obj.rent_accepted_date is not None:
                    raise ValidationError

                # 반납 중 테이블에서 삭제
                renting_obj = Renting.objects.get(log_id=pk)
                renting_obj.delete()

                # 현재 재고에서 개수 더하기
                equip = Equipment.objects.get(model_name=log_obj.model_name.model_name)
                equip.current_stock += log_obj.rent_count
                equip.save()

                # rent_count를 0으로 바꿔버리기
                log_obj.rent_count = 0
                log_obj.save()

                serializer = LogCreateSerializer(log_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "승인 거절할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        except ValidationError:
            return Response({"message": "이미 승인했던 내역이 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Log.DoesNotExist:
            return Response({"message": "내역이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

class ReturnAcceptedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 7-9 반납 승인 API
    def get(self, request, pk):
        try:
            log_obj = Log.objects.get(pk=pk)
            user_obj = User.objects.get(pk=request.user.id)

            #관리자인지 확인
            if request.user.is_staff:
                #승인 가능한 상태인지 확인
                if log_obj.return_accepted_date is not None or log_obj.return_requested_date is None or log_obj.rent_accepted_date is None:
                    raise ValidationError

                # 반납 승인시간 업데이트
                log_obj.return_accepted_date = timezone.now()
                log_obj.save()

                # 반납 중 테이블에서 삭제
                returning_obj = Returning.objects.get(log_id=pk)
                returning_obj.delete()

                # 반납 완료 테이블에 삽입
                Returned.objects.create(
                    log_id=log_obj,
                    return_accepted_date=log_obj,
                    user_id = user_obj
                )

                # 현재 재고에서 개수 더하기
                equip = Equipment.objects.get(model_name=log_obj.model_name.model_name)
                equip.current_stock -= log_obj.rent_count
                equip.save()

                serializer = LogCreateSerializer(log_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "반납 승인할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError:
            return Response({"message": "승인했던 내역이 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Log.DoesNotExist:
            return Response({"message": "내역이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)


class ReturnRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 7-8 반납 신청 API
    def get(self, request, pk):
        try:
            log_obj = Log.objects.get(pk=pk)
            user_obj = User.objects.get(pk= request.user.id)

            #빌린 본인인지 확인
            if log_obj.user_id.id == request.user.id:
                # 반납 가능한 상태인지 확인
                if log_obj.return_requested_date is not None or log_obj.rent_accepted_date is None:
                    raise ValidationError

                #반납 신청시간 업데이트
                log_obj.return_requested_date = timezone.now()
                log_obj.save()

                #대여 중 테이블에서 삭제
                renting_obj = Renting.objects.get(log_id= pk)
                renting_obj.delete()

                #반납 중 테이블에 삽입
                Returning.objects.create(
                    log_id = log_obj,
                    user_id= user_obj,
                )

                serializer = LogCreateSerializer(log_obj)

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "반납 신청할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError:
            return Response({"message": "반납 가능한 상태가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Log.DoesNotExist:
            return Response({"message": "내역이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)


class ExtensionDateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 7-6 반납 기한 연장 API
    def put(self, request, pk):
        try:
            data = request.data.copy()
            log_obj = Log.objects.get(pk=pk)
            if 'extend_date' in data:
                if int(data['extend_date']) < 1 or int(data['extend_date']) >7:
                    raise ValidationError

            if log_obj.user_id.id == request.user.id:
                serializer = LogModifySerializer(log_obj, data=data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "기한 연장할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except Log.DoesNotExist:
            return Response({"message": "내역이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response({"message": "연장은 1~7일 사이로만 가능합니다."}, status= status.HTTP_400_BAD_REQUEST)

class OverDueAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 7-5 나의 연체된 로그 조회
    def get(self,request):
        try:
            log_obj = Log.objects.filter(user_id= request.user.id, return_requested_date__isnull= True,return_deadline__lt=timezone.now())

            if len(log_obj) == 0:
                raise ValidationError

            serializer = LogCreateSerializer(log_obj, many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except ValidationError:
            return Response({"message": "연체된 내역이 없습니다."}, status=status.HTTP_204_NO_CONTENT)

class RentAcceptedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #7-7 대여 승인 API
    def put(self, request, pk):
        try:
            data = request.data.copy()
            if request.user.is_staff:
                r = Log.objects.get(pk=pk)

                #이미 승인되어 있는 경우 예외처리
                if r.rent_accepted_date is not None:
                    raise ValidationError

                serializer_log = LogRentAcceptedSerializer(r, data=data, partial=True)

                if serializer_log.is_valid():
                    serializer_log.save()

                    #대여 횟수 1 더하기
                    b = Equipment.objects.get(pk=r.model_name.model_name)
                    b.total_rent += 1
                    b.save()

                    return Response(serializer_log.data, status=status.HTTP_200_OK)
                return Response(serializer_log.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "대여 요청을 승인할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except Log.DoesNotExist:
            return Response({"message": "내역이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response({"message": "이미 승인한 내역이 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)

class RentRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 7-1 대여 신청 API
    def post(self, request):
        try:
            data = request.data.copy()
            data['user_id'] = request.user.id
            data['return_deadline'] = timezone.now() + timezone.timedelta(days=7)
            data['rent_requested_date'] = timezone.now()

            equip = Equipment.objects.get(model_name=data['model_name'])

            data['rent_price'] = equip.price

            #재고 판단
            if equip.current_stock < int(data['rent_count']):
                raise ValidationError

            #현재 재고에서 개수 빼기
            equip.current_stock -= int(data['rent_count'])
            equip.save()

            serializer_log = LogCreateSerializer(data=data)

            if serializer_log.is_valid():
                serializer_log.save()

                #renting 테이블에 승인일자가 NULL인 채로 삽입

                rent_data = {
                    "user_id": serializer_log.data['user_id'],
                    "log_id": serializer_log.data['id']
                }

                serializer_rent = RentSerializer(data = rent_data)

                if serializer_rent.is_valid():
                    serializer_rent.save()

                return Response(serializer_log.data, status=status.HTTP_201_CREATED)
            return Response(serializer_log.errors, status= status.HTTP_400_BAD_REQUEST)
        except Equipment.DoesNotExist:
            return Response({"message": "해당 기자재의 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"message": "model_name과 수량을 올바르게 전달하세요."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({"message": "대여 신청한 수량이 현재 재고를 초과합니다."}, status=status.HTTP_400_BAD_REQUEST)


    # 7-4 나의 대여 중인 리스트 조회 API
    def get(self, request):
        try:
            renting_obj = Renting.objects.filter(user_id= request.user.id, rent_accepted_date__isnull= False)

            if len(renting_obj) == 0:
                raise ValidationError

            renting_obj = sorted(renting_obj, key=attrgetter('rent_accepted_date.rent_accepted_date'), reverse=True)
            serializer = RentSerializer(renting_obj, many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except ValidationError:
            return Response({"message": "내가 대여 중인 내역이 없습니다."}, status= status.HTTP_204_NO_CONTENT)


class LogAPIView(APIView):
    #6-1 입출고 현황 조회 API
    def get(self, request):
        log_objects = Log.objects.all().order_by('-updated_at')

        if not log_objects.exists():
            return Response({"message": "로그 데이터가 없습니다."}, status= status.HTTP_204_NO_CONTENT)

        serializer = LogCreateSerializer(log_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookmarkLogAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 6-2 현재 로그인한 유저가 즐겨찾기 해둔 기자재의 로그 내역만 조회 API
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
            serializer = LogCreateSerializer(log_list, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({"message": "해당 유저의 즐겨찾기 기자재 로그가 존재하지 않습니다."}, status= status.HTTP_404_NOT_FOUND)

class InventoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #5-2 전체 기자재 리스트 표시(이름순)
    def get(self, request):
        equip = Equipment.objects.all().order_by('model_name')

        if not equip.exists():
            return Response({"message": "기자재 데이터가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        serializer = EquipmentSerializer(equip, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #5-5 기자재 정보 추가 API
    def post(self, request):
        try:
            data = request.data.copy()

            if request.user.is_staff:
                # 기자재 중복체크 필요
                get_object_or_404(Equipment, pk=data['model_name'])

                return Response({"message": "중복된 기자재를 입력했습니다."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "기자재를 추가할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except Http404:
            equipment = data
            serializer = EquipmentSerializer(data=equipment)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"message": "model_name을 올바르게 전달하세요."}, status=status.HTTP_400_BAD_REQUEST)


    # 5-6 기자재 정보 수정 API
    def put(self, request):
        try:
            data = request.data.copy()
            if request.user.is_staff:
                equip = Equipment.objects.get(pk =data['model_name'])

                serializer = EquipmentSerializer(equip, data=data, partial=True)

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
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 5-1 기자재 정보 조회 API
    def get(self, request, pk):
        try:
            equip = Equipment.objects.get(pk=pk)
            serializer = EquipmentSerializer(equip)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Equipment.DoesNotExist:
            return Response({"message": "해당 기자재의 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

    # 5-7 기자재 정보 삭제 API
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
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 5-4 기자재 정보 조회 API(총 조회수 많은 순서)
    def get(self, request):
        equip = Equipment.objects.all().order_by('-total_rent')

        if not equip.exists():
            return Response({"message": "기자재 데이터가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        serializer = EquipmentSerializer(equip, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InventoryInqUpdatedAtAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #5-3 기자재 정보 조회 API(기자재 정보 추가된 시간 순서)
    def get(self, request):
        equip = Equipment.objects.all().order_by('-updated_at')

        if not equip.exists():
            return Response({"message": "기자재 데이터가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        serializer = EquipmentSerializer(equip, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InventorySearchAPIView(APIView):
    # 5-8 기자재 검색 API (model_name,name,type,repository,manufacturer)
     def post(self, request):
         try:
            data = request.data.copy()
            if not data['searchData']:
                equip = Equipment.objects.all()
                serializer = EquipmentSerializer(equip, many=True)
                return Response(serializer.data, status= status.HTTP_200_OK)

            search = data['searchData']
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




