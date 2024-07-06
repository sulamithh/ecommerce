from django.contrib import admin
from django.urls import path, include
from cart.views import CartItemListCreateView, CartItemDetailUpdateDeleteView, SubmitOrderView
from orders.views import OrderListCreateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('products/', include('products.urls')),
    path('cart/cartitems/', CartItemListCreateView.as_view(), name='cartitem-create'),
    path('cart/cartitems/<int:pk>/', CartItemDetailUpdateDeleteView.as_view(), name='cartitem-delete'),
    path('orders/<int:pk>/submit/', SubmitOrderView.as_view(), name='submit-order'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
