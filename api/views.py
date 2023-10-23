
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Menu.models import Group, Category, Addons, OrderStatus, FoodItems, FoodItemGroups, FoodItemCategories, FoodImage
from ProfileSetup.models import PrivateInformation, PublicInformation, RestorantImage, OrderOptionDetail, PaymentOptionDetail, SettlementModeDetail, SettlementTypeDetail, WorkingTimeDetail
from api.serializers import GroupSerializer, CategorySerializer, AddonSerializer, OrderStatusSerializer, FoodItemsSerializer, FoodItemGroups, FoodItemCategories, PrivateInformationSerializer, PublicInformationSerializer
from django.core.exceptions import ValidationError
from rest_framework import serializers
import random
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)    

# Group API Section

@api_view(['POST'])
def send_otp(request):
    mobile_number = request.data.get('mobile_number')
    if not mobile_number:
        return Response({'error': 'Mobile number is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate and send OTP (you might use SMS gateway or other means here)
    otp = str(random.randint(100000, 999999))
    # For simplicity, we're storing OTP in the database, but you should use a cache system like Redis for better performance.
    user, created = UserProfile.objects.get_or_create(mobile_number=mobile_number)
    user.otp = otp
    user.save()

    return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def verify_otp(request):
    mobile_number = request.data.get('mobile_number')
    otp_entered = request.data.get('otp')

    if not mobile_number or not otp_entered:
        return Response({'error': 'Mobile number and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = UserProfile.objects.get(mobile_number=mobile_number, otp=otp_entered)
        user.is_verified = True
        user.save()
        return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


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


# Addon API Section    

@api_view(["GET"])
def addonList(request):
    if request.method == 'GET':
        addons = Addons.objects.all()
        serializer = AddonSerializer(addons, many=True)
        return Response(serializer.data)

@api_view(["POST"])
def addonStore(request):
    if request.method == "POST":
        serializer = AddonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Addon created successfully", "addon": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(["GET"])
def addonEdit(request, id):
    if request.method == "GET":
        addon = Addons.objects.get(id = id)
        serializer = AddonSerializer(addon)
        return Response({"message": "Addon retrieved successfully", "addon": serializer.data}, status = 200)

@api_view(["PUT"])
def addonUpdate(request, id):
    if request.method == "PUT":
        serializer = AddonSerializer(Addons.objects.get(id = id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Addon updated successfully", "addon": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def addonDelete(request, id):
    if request.method == 'DELETE':
        Addons.objects.get(id = id).delete()
        return Response({"message": "Addon deleted successfully"}, status = status.HTTP_204_NO_CONTENT)
    
# Order Status API Section    

@api_view(["GET"])
def orderStatusList(request):
    if request.method == 'GET':
        orderStatus = OrderStatus.objects.all()
        serializer = OrderStatusSerializer(orderStatus, many=True)
        return Response(serializer.data)

@api_view(["POST"])
def orderStatusStore(request):
    if request.method == "POST":
        serializer = OrderStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order Status created successfully", "orderStatus": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(["GET"])
def orderStatusEdit(request, id):
    if request.method == "GET":
        orderStatus = OrderStatus.objects.get(id = id)
        serializer = OrderStatusSerializer(orderStatus)
        return Response({"message": "Order Status retrieved successfully", "orderStatus": serializer.data}, status = 200)

@api_view(["PUT"])
def orderStatusUpdate(request, id):
    if request.method == "PUT":
        serializer = OrderStatusSerializer(OrderStatus.objects.get(id = id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order Status updated successfully", "category": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def orderStatusDelete(request, id):
    if request.method == 'DELETE':
        OrderStatus.objects.get(id = id).delete()
        return Response({"message": "Order Status deleted successfully"}, status = status.HTTP_204_NO_CONTENT)

# Food Items API Section    

@api_view(["GET"])
def foodItemsList(request):
    if request.method == 'GET':
        foodItems = FoodItems.objects.all()
        serializer = FoodItemsSerializer(foodItems, many=True)

        return Response(serializer.data)

@api_view(["POST"])
def foodItemStore(request):
    if request.method == "POST":
        serializer = FoodItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Food Item created successfully", "foodItem": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(["GET"])
def foodItemEdit(request, id):
    if request.method == "GET":
        foodItem = FoodItems.objects.get(id = id)
        foodItemImages = FoodImage.objects.get(foodItems = id)
        foodItemCategories = FoodItemCategories.objects.get(foodItems = id)
        foodItemGroups = FoodItemGroups.objects.get(foodItems = id)
        serializer = FoodItemsSerializer(foodItem, foodItemGroups, foodItemCategories, foodItemImages)
        return Response({"message": "Food Item retrieved successfully", "foodItem": serializer.data}, status = 200)

@api_view(["PUT"])
def foodItemUpdate(request, id):
    if request.method == "PUT":
        serializer = FoodItemsSerializer(FoodItems.objects.get(id = id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Food Item updated successfully", "foodItem": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def foodItemDelete(request, id):
    if request.method == 'DELETE':
        FoodItems.objects.get(id = id).delete()
        return Response({"message": "Food Item deleted successfully"}, status = status.HTTP_204_NO_CONTENT)

# Profile API Section    

@api_view(["GET"])
def profileList(request):
    if request.method == 'GET':
        privateInfo = PrivateInformation.objects.all()
        privateSerializer = PrivateInformationSerializer(privateInfo, many=True)
        publicInfo = PublicInformation.objects.all()
        publicSerializer = PublicInformationSerializer(publicInfo, many=True)
        return Response({"privateInfo": privateSerializer.data, "publicInfo": publicSerializer.data})

@api_view(["POST"])
def profileStore(request):
    if request.method == "POST":
        
        privateSerializer = PrivateInformationSerializer(data=request.data)
        
        publicSerializer = PublicInformationSerializer(data=request.data)

        if privateSerializer.is_valid() and publicSerializer.is_valid():    
            privateInfo = privateSerializer.save(user=request.user, data=request.data)
            publicInfo = publicSerializer.save(user=request.user, data=request.data)

            for payOption in request.data.get('payment_options'):
                PaymentOptionDetail.objects.create(private_information=privateInfo, payment_option=payOption)
            for orderOpt in request.data.get('order_options'):
                OrderOptionDetail.objects.create(public_information=publicInfo, order_option=orderOpt)
            for settlementType in request.data.get('settlement_types'):
                SettlementTypeDetail.objects.create(private_information=privateInfo, settlement_type=settlementType)
            for settlementMode in request.data.get('settlement_modes'):
                SettlementModeDetail.objects.create(private_information=privateInfo, settlement_mode=settlementMode)    
            for workingTime in request.data.get('working_times'):
                WorkingTimeDetail.objects.create(public_information=publicInfo, working_time=workingTime)

            for image_data in request.data.get('restorant_images'):
                RestorantImage.objects.create(public_information=publicInfo, image=image_data['image'])
        profiles = {
            "privateInfo": privateSerializer.data,
            "publicInfo": publicSerializer.data
        }
        return Response({"message": "Profile created successfully", "profiles": profiles}, status=status.HTTP_201_CREATED)
    return Response({"privateInfoError": privateSerializer.errors, "publicInfoErrors": publicSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(["GET"])
def profileEdit(request, id):
    if request.method == "GET":
        privateInfo = PrivateInformation.objects.get(id=id)
        privateSerializer = PrivateInformationSerializer(privateInfo, many=True)
        publicInfo = PublicInformation.objects.get(id=id)
        publicSerializer = PublicInformationSerializer(publicInfo, many=True)

        profile = {
            "privateInfo": privateSerializer.data, 
            "publicInfo": publicSerializer.data,
        }

        return Response({"message": "Profile retrieved successfully", "profile": profile}, status = 200)

@api_view(["PUT"])
def profileUpdate(request, id):
    if request.method == "PUT":
        privateSerializer = PrivateInformationSerializer(PrivateInformation.objects.get(id = id), data=request.data)
        publicSerializer = PublicInformationSerializer(PublicInformation.objects.get(id = id), data=request.data)

        if privateSerializer.is_valid() and publicSerializer.is_valid():    
            privateInfo = privateSerializer.save(user=request.user, data=request.data)
            publicInfo = publicSerializer.save(user=request.user, data=request.data)

            PaymentOptionDetail.objects.filter(private_information=id).delete()
            for payOption in request.data.get('payment_options'):
                PaymentOptionDetail.objects.create(private_information=privateInfo, payment_option=payOption)
            for orderOpt in request.data.get('order_options'):
                OrderOptionDetail.objects.create(public_information=publicInfo, order_option=orderOpt)
            SettlementTypeDetail.objects.filter(private_information=id).delete()
            for settlementType in request.data.get('settlement_types'):
                SettlementTypeDetail.objects.create(private_information=privateInfo, settlement_type=settlementType)
            SettlementModeDetail.objects.filter(private_information=id).delete()
            for settlementMode in request.data.get('settlement_modes'):
                SettlementModeDetail.objects.create(private_information=privateInfo, settlement_mode=settlementMode)    
            SettlementTypeDetail.objects.filter(public_information=publicInfo).delete()
            for workingTime in request.data.get('working_times'):
                WorkingTimeDetail.objects.create(public_information=publicInfo, working_time=workingTime)
            RestorantImage.objects.filter(public_information=publicInfo).delete()
            for image_data in request.data.get('restorant_images'):
                RestorantImage.objects.create(public_information=publicInfo, image=image_data['image'])
        profiles = {
            "privateInfo": privateSerializer.data,
            "publicInfo": publicSerializer.data
        }
        return Response({"message": "Profile updated successfully", "profiles": profiles})
    return Response({"privateInfoError": privateSerializer.errors, "publicInfoErrors": publicSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def profileDelete(request, id):
    if request.method == 'DELETE':
        PrivateInformation.objects.get(id = id).delete()
        return Response({"message": "Profile deleted successfully"}, status = status.HTTP_204_NO_CONTENT)        