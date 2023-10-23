from django.db import models
from DelivaryBoys.models import DelivaryBoy
from Menu.models import FoodItems

# Create your models here.

class OrderStatus(models.Model):
    name = models.CharField(max_length=255)

class Orders(models.Model):
    order_reference = models.CharField(max_length=100, null=True)
    customer_name = models.CharField(max_length=200, null=True)
    customer_address = models.TextField(null=True)
    customer_email = models.CharField(max_length=200, null=True)
    customer_mobile = models.CharField(max_length=200, null=True)
    customer_balance = models.FloatField()
    order_date = models.DateField(null=True)
    order_time = models.TimeField(null=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    confirm_status = models.IntegerField(null=True)
    delivary_boy = models.ForeignKey(DelivaryBoy, on_delete=models.CASCADE)
    delivary_status = models.CharField(max_length=200, null=True)

class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    item = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200, null=True)
    item_description = models.TextField(null=True)
    item_price = models.FloatField(null=True)
    item_quantity = models.FloatField(null=True)
    total_price = models.FloatField(null=True)
    