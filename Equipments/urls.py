from django.urls import path
from Equipments.views import InventoryAPIView,InventoryDetailAPIView,InventoryInqUpdatedAtAPIView,\
     InventoryInqTotalRentAPIView,InventorySearchAPIView, LogAPIView,BookmarkLogAPIView,RentRequestAPIView,RentAcceptedAPIView,OverDueAPIView,ExtensionDateAPIView,ReturnRequestAPIView, ReturnAcceptedAPIView,RentRefusedAPIView, ReturnedGetAPIView, RequestGetAPIView

from . import views

urlpatterns= [
     #승인 대기 중인 내역 조회
     path('request/', RequestGetAPIView.as_view()),

     #반납 완료된 내역 조회
     path('returned/', ReturnedGetAPIView.as_view()),

     #반납 신청 및 승인
     path('return/request/<int:pk>/', ReturnRequestAPIView.as_view()),
     path('return/accept/<int:pk>/', ReturnAcceptedAPIView.as_view()),

     #대여 신청 및 승인, 거절
     path('rent/request/', RentRequestAPIView.as_view()),
     path('rent/accept/<int:pk>/', RentAcceptedAPIView.as_view()),
     path('rent/refused/<int:pk>/', RentRefusedAPIView.as_view()),

     #연체된 기자재 조회
     path('overdue/', OverDueAPIView.as_view()),

     #대여 기간 연장
     path('extend/<int:pk>/', ExtensionDateAPIView.as_view()),

     #입출고 현황 조회
     path('log/', LogAPIView.as_view()),

     #즐겨찾기 해둔 기자재의 입출고 현황만 조회
     path('log/bookmark/', BookmarkLogAPIView.as_view()),

     #기자재 정보 추가, 삭제, 조회(이름순),조회(가격순),조회(총 대여횟수) 수정
     path('inventory/', InventoryAPIView.as_view()),
     path('inventory/updatedat/',InventoryInqUpdatedAtAPIView.as_view()),
     path('inventory/totalrent/', InventoryInqTotalRentAPIView.as_view()),

     #기자재 검색
     path('inventory/search/', InventorySearchAPIView.as_view()),

     #기자재 상세정보 조회
     path('inventory/<str:pk>/', InventoryDetailAPIView.as_view()),
]