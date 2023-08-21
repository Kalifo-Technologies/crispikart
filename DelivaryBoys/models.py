from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class DelivaryBoy(models.Model):
    name = models.CharField(max_length=200, null=True)
    photo = models.ImageField(upload_to='images/delivary_boys')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=200, null=True)
    place = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)