from rest_framework import serializers
from Menu.models import Group, Category, Addons, OrderStatus, FoodItems, FoodItemGroups, FoodItemCategories, FoodImage
from ProfileSetup.models import PrivateInformation, PublicInformation
from .models import UserProfile
from django.contrib.auth.models import User



# Group Serializer Class

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Replace with your user model
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('mobile_number', 'otp', 'is_verified')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

    def validate_name(self, value):
        
        if self.instance and self.instance.name == value:
            return value
        
        # Check if a group with the given name already exists
        if Group.objects.filter(name=value).exists():
            raise serializers.ValidationError("group already exists with same name")
        return value

# Category Serializer Class

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        
        if self.instance and self.instance.name == value:
            return value
        
        # Check if a group with the given name already exists
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("category already exists with same name")
        return value        

# Addon Serializer Class

class AddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addons
        fields = '__all__'

    def validate_name(self, value):
        
        if self.instance and self.instance.name == value:
            return value
        
        # Check if a group with the given name already exists
        if Addons.objects.filter(name=value).exists():
            raise serializers.ValidationError("Addon already exists with same name")
        return value        
    
class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'       

    def validate_name(self, value):
        
        if self.instance and self.instance.name == value:
            return value
        
        # Check if a group with the given name already exists
        if OrderStatus.objects.filter(name=value).exists():
            raise serializers.ValidationError("order status already exists with same name")
        return value            
    
class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields = ['photo']

class FoodItemGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItemGroups
        fields = ['group']

class FoodItemCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItemCategories
        fields = ['category']

class FoodItemsSerializer(serializers.ModelSerializer):
    groups = FoodItemGroupsSerializer(many=True)
    categories = FoodItemCategoriesSerializer(many=True)
    images = FoodImageSerializer(many=True)

    class Meta:
        model = FoodItems
        fields = ['id', 'name', 'description', 'quantity', 'price', 'service_type', 'groups', 'categories', 'images']
    
class PrivateInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateInformation
        fields = '__all__'    

class PublicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model: PublicInformation
        fields = '__all__'        