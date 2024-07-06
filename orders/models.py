from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from cart.models import CartItem

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def update_total_price(self):
        total_price = sum(item.product.price * item.quantity for item in self.order_items.all())
        Order.objects.filter(pk=self.pk).update(total_price=total_price)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk:
            self.update_total_price()

class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
