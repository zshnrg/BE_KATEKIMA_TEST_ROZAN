from django.urls import path
from . import views

urlpatterns = [
  path('items/', views.ItemsList.as_view(), name='items_list'),
  path('items/<str:code>/', views.ItemsDetail.as_view(), name='items_detail'),
]