from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=200)
    StartTime = models.TimeField(null=True, blank=True)
    EndTime = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/categories')    

    def __str__(self):
        return self.name

class FoodItems(models.Model):
    group_ids = models.IntegerField()
    category_ids = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.CharField(max_length=300)
    quantity = models.FloatField()
    price = models.FloatField()
    availability = models.IntegerField()
    quantity = models.FloatField()

class OrderStatus(models.Model):
    name = models.CharField(max_length=200)    