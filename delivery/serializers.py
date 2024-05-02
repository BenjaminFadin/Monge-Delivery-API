from decimal import Decimal

from django.db import transaction
from rest_framework import serializers
from users.models import User

from delivery.models import (
    Cart,
    CartItem,
    Category, 
    Product, 
    Order, 
    OrderItem, 
    Address
)

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'parent', 'title']

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'title', 
            'unit_price', 
            'inventory', 
            'discount', 
            'is_sale',
            'category'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer', 'items']



class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ['location', 'customer']



class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        # print(self.validated_data['cart_id'])
        # print(self.context['user_id'])
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']

            (customer, created) = User.objects.get_or_create(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects \
                .select_related('product') \
                .filter(cart_id=self.validated_data['cart_id'])
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.delete(pk=cart_id).delete()

