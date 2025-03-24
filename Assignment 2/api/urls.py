from django.urls import path
from .views import items_views as items

urlpatterns = [
  path('items/', items.ItemsList.as_view(), name='items_list'),
  path('items/<str:code>/', items.ItemsDetail.as_view(), name='items_detail'),
]