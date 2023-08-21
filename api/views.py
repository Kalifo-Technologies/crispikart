
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Menu.models import Group, Category
from api.serializers import GroupSerializer, CategorySerializer
from django.core.exceptions import ValidationError
from rest_framework import serializers

# Create your views here.

# Group API Section

@api_view(["GET"])
def groupList(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

@api_view(["POST"])
def groupStore(request):
    if request.method == "POST":
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Group created successfully", "group": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(["GET"])
def groupEdit(request, id):
    if request.method == "GET":
        group = Group.objects.get(id = id)
        serializer = GroupSerializer(group)
        return Response({"message": "Group retrieved successfully", "group": serializer.data}, status = 200)

@api_view(["PUT"])
def groupUpdate(request, id):
    if request.method == "PUT":
        serializer = GroupSerializer(Group.objects.get(id = id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Group updated successfully", "group": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def groupDelete(request, id):
    if request.method == 'DELETE':
        Group.objects.get(id = id).delete()
        return Response({"message": "Group deleted successfully"}, status = status.HTTP_204_NO_CONTENT)
    
# Category API Section    

@api_view(["GET"])
def categoryList(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(["POST"])
def categoryStore(request):
    if request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category created successfully", "category": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(["GET"])
def categoryEdit(request, id):
    if request.method == "GET":
        category = Category.objects.get(id = id)
        serializer = CategorySerializer(category)
        return Response({"message": "Category retrieved successfully", "category": serializer.data}, status = 200)

@api_view(["PUT"])
def categoryUpdate(request, id):
    if request.method == "PUT":
        serializer = CategorySerializer(Category.objects.get(id = id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category updated successfully", "category": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def categoryDelete(request, id):
    if request.method == 'DELETE':
        Category.objects.get(id = id).delete()
        return Response({"message": "Category deleted successfully"}, status = status.HTTP_204_NO_CONTENT)