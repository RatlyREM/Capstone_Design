from django.urls import path

from Accounts.views import UserInfoAPIView, AuthAPIView, SigninAPIView

urlpatterns = [
    path('signin/', SigninAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    #path('info/', UserInfoAPIView.as_view()),
]
