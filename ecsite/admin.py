from django.contrib import admin
from ecsite.models.product import Product, ProductImage
from ecsite.models.order import Order, OrderItem
from ecsite.models.cart import Cart, CartItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
