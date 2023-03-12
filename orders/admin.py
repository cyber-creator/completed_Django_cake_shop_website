from django.contrib import admin
from .models import Order, OrderUnit, DeliveryOption, OrderStatus

# Register your models here.


class OrderUnitInline(admin.TabularInline):
    model = OrderUnit


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'first_name', 'last_name', 'phone', 'email', 'address', 'postal_code', 'city', 'state', 'note',
        'created', 'updated', 'order_status', 'payment_type', 'delivery', 'tracking_code', 'completed']
    list_filter = ['created', 'updated', 'order_status', 'payment_type', 'delivery', 'tracking_code', 'completed']
    list_editable = ['order_status', 'delivery', 'tracking_code', 'completed']
    inlines = [OrderUnitInline]


@admin.register(DeliveryOption)
class DeliveryOptionAdmin(admin.ModelAdmin):
    list_display = ['delivery_type', 'slug', 'price']
    prepopulated_fields = {'slug': ('delivery_type',)}


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['status', 'slug']
    prepopulated_fields = {'slug': ('status',)}


admin.site.register(OrderUnit)
