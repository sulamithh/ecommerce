from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CartItem, Order
from .serializers import CartItemSerializer, AddCartItemSerializer
from orders.serializers import OrderSerializer
from products.models import Product


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemListCreateView(generics.ListCreateAPIView):
    serializer_class = AddCartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(order__user=self.request.user, order__is_active=True)

    def perform_create(self, serializer):
        order, created = Order.objects.get_or_create(user=self.request.user, is_active=True)
        product_name = self.request.data.get('product_name')
        product = get_object_or_404(Product, name=product_name)

        if product.quantity < self.request.data['quantity']:
            raise serializers.ValidationError(f"Not enough stock for product {product.name}")

        serializer.save(order=order, product=product)


class CartItemDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(order__user=self.request.user, order__is_active=True)


class SubmitOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        order.is_active = False
        order.save()
        CartItem.objects.filter(order=order).delete()
        return Response(OrderSerializer(order).data)
