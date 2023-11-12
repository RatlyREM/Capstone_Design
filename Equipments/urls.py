from django.urls import path
from Equipments.views import InventoryAPIView

from . import views

urlpatterns= [
     path('inventory/<str:pk>', InventoryAPIView.as_view()),
]