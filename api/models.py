from django.db import models

# Create your models here.
class UserProfile(models.Model):
    mobile_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
