import jwt
import requests
import rest_framework_simplejwt.exceptions

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication

from Accounts.serializers import UserSerializer, UserInfoSerializer,UserEmailAndNickSerializer,CustomTokenObtainPairSerializer
from Accounts.utils import login_check
from Accounts.models import User, UserInfo
from rest_framework_simplejwt.views import TokenObtainPairView

from config.settings import SECRET_KEY
from django.http import Http404

class CustomTokenObtainPairView(TokenObtainPairView):
    #1-2 이메일 로그인 API
    serializer_class = CustomTokenObtainPairSerializer


class UserInfoCreateAPIView(APIView):
    #2-1 회원가입 과정에서 회원정보 생성 API
    def post(self, request, pk):
        try:
            #해당 유저 정보가 존재하는지 확인
            User.objects.get(pk= pk)

            UserInfo.objects.get(user_id = pk)

            return Response({"message": "유저의 정보가 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "그런 유저는 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except UserInfo.DoesNotExist:
            data = request.data.copy()
            data['user'] = pk
            serializer = UserInfoSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserInfoAPIView(APIView):
    #2-2 로그인한 유저의 개인정보 조회 API
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            userInfo = UserInfo.objects.get(user_id = request.user.id)
            serializer = UserInfoSerializer(userInfo)
            return Response(serializer.data)
        except UserInfo.DoesNotExist:
            failMessage= {
                "message": "해당 유저의 정보가 존재하지 않습니다."
            }
            return Response(failMessage, status=status.HTTP_400_BAD_REQUEST)

    #2-3 로그인한 유저의 name, phone_number, address 수정 가능한 API
    def put(self, request):
        try:
            userInfo = UserInfo.objects.get(user_id=request.user.id)

            serializer = UserInfoSerializer(userInfo, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except UserInfo.DoesNotExist:
            return Response({"message": "해당 유저의 개인정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

class SigninAPIView(APIView):
    # 1-1 email과 password, nickname을 통한 회원가입 API
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # token = TokenObtainPairSerializer.get_token(user)
            # refresh_token = str(token)
            # access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "회원가입 성공",
                    # "token": {
                    #     "access": access_token,
                    #     "refresh": refresh_token,
                    # },
                },
                status=status.HTTP_200_OK
            )

            # res.set_cookie("access", access_token, httponly=True)
            # res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthIDAPIView(APIView):
    #1-6 로그인 유저 정보 조회 API
    def get(self, request, pk):
        try:
            u = User.objects.get(pk=pk)

            serializer = UserEmailAndNickSerializer(u)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "그런 유저는 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    #2-4 회원 탈퇴 API
    def delete(self,request, pk):
        try:
            u = get_object_or_404(User, pk=pk)

            try:
                userInfo = UserInfo.objects.get(user_id= pk)

                # 회원정보 삭제
                userInfo.delete()
            except UserInfo.DoesNotExist:
                pass

            #유저 삭제
            u.delete()

            return Response({"message": "회원탈퇴 완료"}, status= status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"message": "그런 유저는 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class AuthAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 1-4 로그인 상태 확인 API
    def get(self, request):
        try:
            # access = request.COOKIES.get('access')
            # payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            # pk = payload.get('user_id')
            user = request.user
            serializer = UserSerializer(instance=user)
            res = Response({
                "user": serializer.data,
                "message": "로그인 중입니다.",
                },
                status=status.HTTP_200_OK
            )
            # res.set_cookie('access', access)
            # res.set_cookie('refresh', request.COOKIES.get('refresh'))
            return res
        except jwt.exceptions.InvalidTokenError:
            return Response({"message": "로그인이 만료되었습니다. 로그인 해 주세요."}, status=status.HTTP_404_NOT_FOUND)

        # except User.DoesNotExist:
        #     return Response({"message": "로그인 되어 있지 않습니다. 로그인 해 주세요."}, status=status.HTTP_404_NOT_FOUND)
        # access token이 만료되었을 때 -> 클라이언트 단에서 해결 필요, refresh 토큰을 통해 access 재발급
        # except jwt.exceptions.ExpiredSignatureError:
        #     try:
        #         data = {'refresh': request.COOKIES.get('refresh', None)}
        #         serializer = TokenRefreshSerializer(data=data)
        #         if serializer.is_valid(raise_exception=True):
        #             access = serializer.validated_data.get('access', None)
        #             refresh = serializer.validated_data.get('refresh', None)
        #             payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
        #             pk = payload.get('user_id')
        #             user = get_object_or_404(User, pk=pk)
        #             serializer = UserSerializer(instance=user)
        #             res = Response(serializer.data, status=status.HTTP_200_OK)
        #             res.set_cookie('access', access)
        #             res.set_cookie('refresh', refresh)
        #             return res
        #     except rest_framework_simplejwt.exceptions.TokenError:
        #         return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_200_OK)
        #
        #     raise jwt.exceptions.InvalidTokenError
        # 사용 불가능한 토큰일 때
    #1-2 이메일을 통한 로그인 API -> CustomTokenObtainPairAPI로 대체
    # def post(self, request):
        # # user 인증
        # user = authenticate(
        #     username=request.data.get("email"), password=request.data.get("password")
        # )
        #
        # if user is not None:
        #     serializer = UserSerializer(user)
        #
        #     token = TokenObtainPairSerializer.get_token(user)
        #     refresh_token = str(token)
        #     access_token = str(token.access_token)
        #     res = Response(
        #         {
        #             "user": serializer.data,
        #             "message": "Login Success",
        #             "token": {
        #                 "access": access_token,
        #                 "refresh": refresh_token
        #             },
        #         },
        #         status=status.HTTP_200_OK
        #     )
        #
        #     res.set_cookie("access", access_token, httponly=True)
        #     res.set_cookie("refresh", refresh_token, httponly=True)
        #     return res
        # else:
        #     failMessage = {
        #         "message": "아이디 또는 비밀번호가 일치하지 않습니다."
        #     }
        #     return Response(failMessage, status=status.HTTP_400_BAD_REQUEST)

    #1-3 로그아웃 API
    # def delete(self, request):
    #     response= Response({
    #         "message": "로그아웃 성공"
    #     })
    #     response.delete_cookie("access")
    #     response.delete_cookie("refresh")
    #     return response
