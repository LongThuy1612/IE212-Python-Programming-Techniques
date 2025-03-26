from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'motor_type', 'description')
    search_fields = ['name', 'price', 'motor_type']
    list_filter = ('id', 'name', 'price', 'motor_type', 'description')
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'complete', 'transaction_id')
    search_fields = ['customer', 'order_date', 'complete']
    list_filter = ('id', 'customer', 'order_date', 'complete', 'transaction_id')
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'quantity', 'choiced')
    search_fields = ['product', 'order']
    list_filter = ('id', 'product', 'order', 'quantity', 'choiced')
admin.site.register(OrderItem, OrderItemAdmin)

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'reci_name', 'reci_phone', 'address', 'city', 'province', 'date_added')
    search_fields = ['customer', 'order', 'reci_name', 'reci_phone', 'city', 'province', 'date_added']
    list_filter = ('id', 'customer', 'order', 'reci_name', 'reci_phone', 'address', 'city', 'province', 'date_added')
admin.site.register(ShippingAddress, ShippingAdmin)