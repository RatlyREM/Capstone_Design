from django.urls import path

from Accounts.views import UserInfoAPIView, AuthAPIView, SigninAPIView,AuthIDAPIView,UserInfoCreateAPIView

urlpatterns = [
    #회원가입
    path('signin/', SigninAPIView.as_view()),

    #로그인, 로그인 상태 확인, 로그아웃
    path('auth/', AuthAPIView.as_view()),

    #회원 탈퇴 및 유저 아이디에 따른 닉네임, 이메일 확인
    path('auth/<int:pk>/', AuthIDAPIView.as_view()),

    #회원 개인정보 생성,조회,수정
    path('info/', UserInfoAPIView.as_view()),
    path('info/<int:pk>/', UserInfoCreateAPIView.as_view()),

]
