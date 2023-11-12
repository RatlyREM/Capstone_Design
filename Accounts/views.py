import jwt

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from Accounts.serializers import UserSerializer
from Accounts.utils import login_check
from Accounts.models import User

from config.settings import SECRET_KEY


class UserInfoAPIView(APIView):
    @login_check
    def get(self, request):
        return Response("hello")


class SigninAPIView(APIView):
    # email과 password, nickname을 통한 회원가입 API
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "Signin Success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK
            )

            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):
    # 로그인 상태 확인 API
    def get(self, request):
        try:
            access = request.COOKIES.get('access')
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            res = Response(serializer.data, status= status.HTTP_200_OK)

            res.set_cookie('access', access)
            res.set_cookie('refresh', request.COOKIES.get('refresh'))
            return res
        except User.DoesNotExist:
            return Response({"message": "로그인 되어 있지 않습니다. 로그인 해 주세요."}, status=status.HTTP_404_NOT_FOUND)

    # 이메일을 통한 로그인 API
    def post(self, request):
        # user 인증
        user = authenticate(
            username=request.data.get("email"), password=request.data.get("password")
        )

        if user is not None:
            serializer = UserSerializer(user)

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "Login Success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token
                    },
                },
                status=status.HTTP_200_OK
            )

            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            failMessage = {
                "message": "아이디 또는 비밀번호가 일치하지 않습니다."
            }
            return Response(failMessage, status=status.HTTP_400_BAD_REQUEST)
