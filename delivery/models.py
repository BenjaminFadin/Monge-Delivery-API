from django.db import models
from django.core.validators import MinValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from uuid import uuid4

from shared.models import BaseModel


class Promotion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    picture = models.ImageField(upload_to='promotion_images/', null=True, blank=True)
    video = models.FileField(upload_to='promotion_videos/', null=True, blank=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Category(BaseModel, MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Categories'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')
    unit_price = models.FloatField()
    inventory = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    discount = models.IntegerField(default=0)
    is_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
 

class Order(BaseModel):
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_OUT_FOR_DELIVERY = 'O'    
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_OUT_FOR_DELIVERY, 'Out for delivery'),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]
    
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    courier = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='courier_orders', limit_choices_to={'is_courier': True}, null=True, blank=True)
    recipient = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='recipient_orders', limit_choices_to={'is_courier': False}, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.get_payment_status_display()}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.CharField(max_length=30)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='carts')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")  # rather thans cartitem_set
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], default=1
    )

    def __str__(self):
        return self.product.title
    
    class Meta:
        unique_together = [['cart', 'product']]


class Address(BaseModel):
    title = models.CharField(max_length=200)
    pickup_location = models.CharField(max_length=255)
    delivery_location = models.CharField(max_length=255)
    customer = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)


class Comment(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='comment')
    rating_star = models.IntegerField(default=0)
    content = models.TextField()

    def __str__(self):
        return f"{self.author}'s comment"


