from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PrivateInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='images/profile', null=True)
    owner_name = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=200)
    whatsapp_no = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=255, null=True)
    established_year = models.IntegerField(null=True)
    no_of_employees = models.IntegerField(null=True)
    manager_name = models.CharField(max_length=250)
    manager_contact_no = models.CharField(max_length=200)

    def __str__(self):
        return self

class PublicInformation(models.Model):

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
    images = models.ImageField(upload_to='images/restorant', null=True)

class WorkingTimeDetail(models.Model):
    public_information = models.ForeignKey(PublicInformation, on_delete=models.CASCADE)        
    working_time = models.CharField(max_length=100, null=True)

class PaymentOption(models.Model):
    private_information = models.ForeignKey(PrivateInformation, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class SettlementType(models.Model):
    private_information = models.ForeignKey(PrivateInformation, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class SettlementMode(models.Model):
    private_information = models.ForeignKey(PrivateInformation, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class OrderOption(models.Model):
    public_information = models.ForeignKey(PublicInformation, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)