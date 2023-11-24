from django.urls import path
from Equipments.views import InventoryAPIView,InventoryDetailAPIView,InventoryInqUpdatedAtAPIView,\
     InventoryInqTotalRentAPIView,InventorySearchAPIView, LogAPIView,BookmarkLogAPIView,RentRequestAPIView,RentAcceptedAPIView,OverDueAPIView


from . import views

urlpatterns= [
     #대여 신청 및 승인
     path('rent/', RentRequestAPIView.as_view()),
     path('rent/<int:pk>/', RentAcceptedAPIView.as_view()),

     #연체된 기자재 조회
     path('overdue/', OverDueAPIView.as_view()),

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