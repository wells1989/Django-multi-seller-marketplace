from django.contrib import admin
from .models import Product, OrderDetail

# Register your models here.
admin.site.register(Product)
admin.site.register(OrderDetail)
