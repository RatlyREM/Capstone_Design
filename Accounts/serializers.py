from rest_framework import serializers

from Accounts.models import User, UserInfo
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import jwt
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.response import Response

from Accounts.models import User
from config.settings import SECRET_KEY

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod

    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id
        token['email'] = user.email
        token['nickname'] = user.nickname
        token['is_staff'] = user.is_staff

        return token

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user= User.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password']
        )
        return user
    class Meta:
        model = User
        fields = ['id' ,'password', 'last_login','email', 'nickname','is_superuser', 'is_active', 'is_staff', 'created_at', 'updated_at']

class UserEmailAndNickSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id', 'nickname', 'email']

class UserInfoSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)

        instance.save()
        return instance
    class Meta:
        model= UserInfo
        fields = '__all__'