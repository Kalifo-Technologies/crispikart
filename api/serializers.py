from rest_framework import serializers
from Menu.models import Group, Category

# Group Serializer Class

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