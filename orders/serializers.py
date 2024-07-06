from rest_framework import serializers
from .models import Order, CartItem
from cart.serializers import CartItemSerializer

class OrderSerializer(serializers.ModelSerializer):
    order_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'total_price', 'is_active', 'order_items']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'order', 'product', 'quantity']
3