from django.urls import path
from Equipments.views import InventoryAPIView,InventoryDetailAPIView,InventoryInqUpdatedAtAPIView,InventoryInqTotalRentAPIView,InventorySearchAPIView, LogAPIView

from . import views

urlpatterns= [
     #입출고 현황 조회
     path('log/', LogAPIView.as_view()),


     #기자재 정보 추가, 삭제, 조회(이름순),조회(가격순),조회(총 대여횟수) 수정
     path('inventory/', InventoryAPIView.as_view()),
     path('inventory/updatedat/',InventoryInqUpdatedAtAPIView.as_view()),
     path('inventory/totalrent/', InventoryInqTotalRentAPIView.as_view()),

     #기자재 검색
     path('inventory/search/', InventorySearchAPIView.as_view()),

     #기자재 상세정보 조회
     path('inventory/<str:pk>/', InventoryDetailAPIView.as_view()),
]