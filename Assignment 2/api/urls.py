from django.urls import path
from .views import items_view as items
from .views import purchases_view as purchases

urlpatterns = [
  path('items/', items.ItemsList.as_view(), name='items_list'),
  path('items/<str:code>/', items.ItemsDetail.as_view(), name='items_detail'),

  path('purchases/', purchases.PurchasesList.as_view(), name='purchases_list'),
  path('purchases/<str:code>/', purchases.Purchase.as_view(), name='purchase'),
  path('purchases/<str:header_code>/details/', purchases.PurchaseDetails.as_view(), name='purchase_details')
]