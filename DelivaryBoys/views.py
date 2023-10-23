from django.shortcuts import render, redirect
from django.contrib import messages
from DelivaryBoys.models import DelivaryBoy
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
import re

def index(request):
    
    items_per_page = 10
    delivaryBoys = DelivaryBoy.objects.all()
    paginator = Paginator(delivaryBoys, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    nums = 'a' * page_obj.paginator.num_pages

    delivaryBoysCount = DelivaryBoy.objects.count()

    context = {
        "nums": nums,
        "page_obj": page_obj,
        "delivaryBoysCount": delivaryBoysCount,
        "page_number": page_number
    }
    
    return render(request, 'pages/delivary_boys/index.html', context)

def addDelivaryBoy(request):

        try:
            if request.method == "POST":

                req = request.POST

                name = req.get('name')
                place = req.get('place')
                photo = request.FILES.get('photo')
                mobile_no = req.get('mobile_no')
                username = req.get('username')
                password = req.get('password')
                confirm_password = req.get('confirm_password')
                hashed_password = make_password(password)

                errors = {}

                if not name:
                    errors['name'] = 'name field is required'
                if not place:
                    errors['place'] = 'place field is required'
                if not mobile_no:
                    errors['mobile_no'] = 'Mobile no field is required'
                if not validate_mobile_number(mobile_no):   
                    errors['mobile_no'] = 'Invalid mobile no.'    
                if not username:
                    errors['username'] = 'Username field is required'
                if DelivaryBoy.objects.filter(username = username).exists():
                    errors['username'] = 'Username is already exist'             
                if not password:
                    errors['password'] = 'Password field is required'     
                if password != confirm_password:
                    errors['password'] = 'Passwords do not match.'    
                
                if errors:
                    return JsonResponse(errors, status=400)        
                
                DelivaryBoy.objects.create(
                    user = request.user,
                    name = name,
                    photo = photo,
                    place = place,
                    mobile_no = mobile_no,
                    username = username,
                    password = hashed_password
                )

                return JsonResponse({"message": "Delivary Boy created successfully"})
            
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=500)
            
        
    
def editDelivaryBoy(request):

    try:    
        if request.method == "POST":
            
            req = request.POST
            
            edit_id = req.get('edit_id')
            name = req.get('name')
            place = req.get('place')
            mobile_no = req.get('mobile_no')

            errors = {}

            if not name:
                errors['name'] = 'name field is required'
            if not place:
                errors['place'] = 'place field is required'
            if not mobile_no:
                errors['mobile_no'] = 'Mobile no field is required'
            if not validate_mobile_number(mobile_no):   
                errors['mobile_no'] = 'Invalid mobile no.'    

            if errors:
                return JsonResponse(errors, status=400)        

            delivaryBoy = DelivaryBoy.objects.get(id = edit_id)
            photo = request.FILES.get('photo', delivaryBoy.photo)
            delivaryBoy.user = request.user
            delivaryBoy.name = name
            delivaryBoy.photo = photo 
            delivaryBoy.place = place
            delivaryBoy.mobile_no = mobile_no
            delivaryBoy.save()

            return JsonResponse({"message": "Delivary Boy updated successfully"})
            
    except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=500)    
    

def deleteDelivaryBoy(request):
    delete_id = request.POST.get('delete_id')
    group = DelivaryBoy.objects.get(id = delete_id)
    group.delete()
    
    return JsonResponse({"message": "Delivary Boy deleted successfully"})


def validate_mobile_number(mobile_number):

    pattern = r'^\d{10}$'
    return re.match(pattern, mobile_number)        
