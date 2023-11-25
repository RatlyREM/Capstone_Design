import jwt
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.response import Response

from Accounts.models import User
from config.settings import SECRET_KEY


def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access = request.COOKIES.get('access')
            payload = jwt.decode(access, SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return Response({'message': '먼저 로그인해 주십시오.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'INVALID USER'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"message": "다시 로그인해 주십시오."}, status=status.HTTP_400_BAD_REQUEST)
        return func(self, request, *args, **kwargs)

    return wrapper