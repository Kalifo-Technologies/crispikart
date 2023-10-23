from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PrivateInformation(models.Model):
    super_admin = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='images/profile/', null=True)
    owner_name = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=200)
    whatsapp_no = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=255, null=True)
    established_year = models.IntegerField(null=True)
    no_of_employees = models.IntegerField(null=True)
    manager_name = models.CharField(max_length=250)
    manager_contact_no = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField()
    
    def __str__(self):
        return self

class PublicInformation(models.Model):
    super_admin = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    private_information = models.ForeignKey(PrivateInformation, on_delete=models.CASCADE)
    restorant_name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=300, null=True)
    contact_no = models.CharField(max_length=200, null=True)
    whatsapp_no = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self

class RestorantImage(models.Model):
    public_information = models.ForeignKey(PublicInformation, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/restorant/', null=True)

class WorkingTimeDetail(models.Model):
    public_information = models.ForeignKey(PublicInformation, on_delete=models.CASCADE)        
    working_time = models.IntegerField(null=True)

class PaymentOptionDetail(models.Model):
    private_information = models.ForeignKey(PrivateInformation, on_delete=models.CASCADE)
    payment_option = models.IntegerField(null=True)

class SettlementTypeDetail(models.Model):
    private_information = models.ForeignKey(PrivateInformation, on_delete=models.CASCADE)
    settlement_type = models.IntegerField(null=True)

class SettlementModeDetail(models.Model):
    private_information = models.ForeignKey(PrivateInformation, on_delete=models.CASCADE)
    settlement_mode = models.IntegerField(null=True)

class OrderOptionDetail(models.Model):
    public_information = models.ForeignKey(PublicInformation, on_delete=models.CASCADE)
    order_option = models.IntegerField(null=True)