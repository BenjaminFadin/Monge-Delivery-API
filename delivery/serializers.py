from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from delivery.models import (
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
            'category', 
            'discount', 
            'is_sale'
        ]
        
class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['placed_at', 'payment_status', 'customer']

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'unit_price']
        
class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ['location', 'customer']
