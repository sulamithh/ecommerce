from django.urls import path
from .views import OrderListCreateView, CartItemListCreateView, CartItemDetailUpdateDeleteView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('cartitems/', CartItemListCreateView.as_view(), name='cartitem-list-create'),
    path('cartitems/<int:pk>/', CartItemDetailUpdateDeleteView.as_view(), name='cartitem-detail-update-delete'),
]
