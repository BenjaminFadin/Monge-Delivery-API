from django.contrib import admin
from django.contrib.auth.models import User, Group
from mptt.admin import MPTTModelAdmin

from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',  'placed_at', 'payment_status', 'courier', 'recipient']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price', 'inventory', 'discount', 'is_sale']

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Promotion)
admin.site.register(Comment)

admin.site.register(Cart)
admin.site.register(CartItem)
