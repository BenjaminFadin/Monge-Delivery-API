from decimal import Decimal

from django.db import transaction
from rest_framework import serializers
from users.models import User

from delivery.models import (
    Promotion,
    Cart,
    CartItem,
    Category, 
    Product, 
    Order, 
    OrderItem, 
    Address
)
from users.serializers import SimpleUserSerializer

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'logo']



class SubCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'parent', 'title', 'logo']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id', 
            'title',
            'image',
            'unit_price', 
            'inventory', 
            'discount', 
            'is_sale',
            'category'
        ]


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['created_at', 'title', 'content', 'picture', 'video', 'is_sent']


class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']
        read_only_fields = ('order',)


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('longitude', 'latitude', 'customer', 'order')
        extra_kwargs = {
            'customer': {'required': False},
            'order': {'required': False}
        }


class OrderSerializer(serializers.ModelSerializer):
    recipient_tg_id = serializers.IntegerField(write_only=True)
    recipient_info = serializers.SerializerMethodField()
    items = OrderItemCreateSerializer(many=True)
    address = OrderAddressSerializer()

    def get_recipient_info(self, obj: Order):
        return SimpleUserSerializer(obj.recipient).data

    class Meta:
        model = Order
        fields = [
            'id', 'placed_at', 'payment_status', 'recipient',
            'items', 'total_price', 'recipient_tg_id', 'recipient_info', 'address'
        ]
        read_only_fields = ('payment_status', 'total_price')

    def create(self, validated_data):
        address_info = validated_data.get('address')
        if not address_info:
            raise serializers.ValidationError({'address': 'This field is required'})
        items = validated_data.get('items')
        if not items:
            raise serializers.ValidationError({'items': 'This field is required'})
        recipient_tg_id = validated_data.get('recipient_tg_id')
        if not recipient_tg_id:
            raise serializers.ValidationError({'recipient_tg_id': 'This field is required'})
        try:
            user = User.objects.get(telegram_id=recipient_tg_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({'recipient_tg_id': "Invalid"})
        validated_data.pop('recipient_tg_id')
        validated_data.pop('items')
        validated_data.pop('address')
        validated_data['recipient'] = user
        order = super().create(validated_data)
        address_info['customer'] = user.id
        address_info['order'] = order.id
        address_serializer = OrderAddressSerializer(data=address_info)
        address_serializer.is_valid(raise_exception=True)
        address_serializer.save()
        for item in items:
            item['order'] = order.id
            item['product'] = item['product'].id
        item_serializer = OrderItemSerializer(data=items, many=True)
        item_serializer.is_valid(raise_exception=True)
        item_serializer.save()
        order.total_price = sum([item.quantity * item.product.unit_price for item in order.items.all()])
        order.save()
        return order


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ['location', 'customer']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    telegram_id = serializers.CharField(write_only=True)
    user = SimpleUserSerializer(read_only=True)

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'telegram_id', 'items', 'total_price', 'user']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    # validate uchun yani biror xato narsa kirgizsa xatolik qaytaradi error emas debugdagi
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # update an existing item
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem    
        fields = ['quantity']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            (customer, created) = User.objects.get_or_create(user_id=user_id)
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects \
                .select_related('product') \
                .filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()
            return order
        
