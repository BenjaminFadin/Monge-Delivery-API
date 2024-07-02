from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',  'placed_at', 'payment_status', 'customer']

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Promotion)
admin.site.register(Comment)

admin.site.register(Cart)
admin.site.register(CartItem)

