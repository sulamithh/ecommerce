from rest_framework import serializers
from .models import Order, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'order', 'product', 'product_name', 'product_price', 'quantity']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['product_name', 'quantity']

    def validate(self, data):
        product_name = data.get('product_name')
        quantity = data.get('quantity')

        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with name {product_name} does not exist")

        if quantity > product.quantity:
            raise serializers.ValidationError(f"Not enough stock for product {product_name}")

        data['product'] = product
        return data

    def create(self, validated_data):
        order = validated_data.get('order')
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        cart_item, created = CartItem.objects.get_or_create(order=order, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        product.quantity -= quantity
        product.save()

        return cart_item

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'total_price', 'is_active', 'items']
