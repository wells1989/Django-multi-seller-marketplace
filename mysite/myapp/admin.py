from django.contrib import admin
from .models import Product, OrderDetail, Cart, CartItem

# Register your models here.
admin.site.register(Product)
admin.site.register(OrderDetail)
admin.site.register(Cart)
admin.site.register(CartItem)
