from django.urls import path

from Bookmark.views import FavoritesAPIView,FavoritesDeleteAPIView
from . import views

urlpatterns= [
     #내 즐겨찾기 목록 조회, 추가, 삭제
     path('box/', FavoritesAPIView.as_view()),
     path('box/<str:pk>', FavoritesDeleteAPIView.as_view()),

]