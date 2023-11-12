from rest_framework import serializers

from Accounts.models import User, UserInfo
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


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserInfo
        fields = '__all__'