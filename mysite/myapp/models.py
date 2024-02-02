from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    seller= models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    file = models.FileField(upload_to="uploads")
    total_sales_amount = models.FloatField(default=0)
    total_sales = models.IntegerField(default = 0) # initialising both this and above as 0, i.e. when created total sales and number of orders for product should be 0


    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    customer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    stripe_payment_intent = models.CharField(max_length=200)# (id that stripe associates with the order) allows you to check the order has been paid by cross referencing this in stripe system
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)