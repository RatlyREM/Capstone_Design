from django.urls import path
from Equipments.views import InventoryAPIView,InventoryDetailAPIView

from . import views

urlpatterns= [
     path('inventory/<str:pk>/', InventoryDetailAPIView.as_view()),
     path('inventory/', InventoryAPIView.as_view()),
]