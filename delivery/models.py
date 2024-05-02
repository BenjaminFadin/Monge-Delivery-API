from django.db import models
from django.core.validators import MinValueValidator
from mptt.models import MPTTModel, TreeForeignKey


from shared.models import BaseModel


class Category(BaseModel, MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Categories'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=255)
    unit_price = models.CharField(max_length=15)
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
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey('users.User', on_delete=models.PROTECT)
    # ichidan reverse related objectni chaqirish uchun bu yerda order.orderitem_set.quantity deb olinadi.
    # related name bilan order.items




class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")  # rather thans cartitem_set
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.CharField(max_length=30)


class Address(BaseModel):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    customer = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

