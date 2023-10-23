from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=200)
    StartTime = models.TimeField(null=True)
    EndTime = models.TimeField(null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/categories')    

    def __str__(self):
        return self.name

class Addons(models.Model):
    name = models.CharField(max_length=200, null=True)
    photo = models.ImageField(upload_to='images/addons', null=True)    

    def __str__(self):
        return self.name

class Availabilities(models.Model):
    name = models.CharField(max_length=200, null=True)    

class FoodItems(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    quantity = models.FloatField()
    price = models.FloatField()
    service_type = models.CharField(max_length=100, null=True)

     # ManyToManyField for images, categories, and groups
    images = models.ManyToManyField('FoodImage')
    categories = models.ManyToManyField(Category)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.name

class FoodItemGroups(models.Model):
    foodItems = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)     

class FoodItemCategories(models.Model):
    foodItems = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)   

class FoodItemAddons(models.Model):
    foodItems = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    addon = models.ForeignKey(Addons, on_delete=models.CASCADE)       

class FoodImage(models.Model):
    foodItems = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/foodItems/', null=True)

    def __str__(self):
        return f"Image {self.id} for Food Item {self.fooditem.name}"

class FoodItemAvailabilities(models.Model):
    foodItems = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    availability = models.ForeignKey(Availabilities, on_delete=models.CASCADE)

class OrderStatus(models.Model):
    name = models.CharField(max_length=200)    

class PaymentOption(models.Model):
    name = models.CharField(max_length=200, null=True)
    
class OrderOption(models.Model):
    name = models.CharField(max_length=200, null=True)

class SettlementType(models.Model):
    name = models.CharField(max_length=200, null=True)

class SettlementMode(models.Model):
    name = models.CharField(max_length=200, null=True)

class WorkingTime(models.Model):
    name = models.CharField(max_length=200, null=True)    
