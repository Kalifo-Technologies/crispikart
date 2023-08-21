from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import re

def index(request):

    items_per_page = 10
    users = User.objects.all()
    paginator = Paginator(users, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    nums = 'a' * page_obj.paginator.num_pages

    usersCount = User.objects.count()

    context = {
        "nums": nums,
        "page_obj": page_obj,
        "usersCount": usersCount,
        "page_number": page_number
    }

    return render(request, 'pages/users/index.html', context)

def addUser(request):
     
    try:

        if request.method == 'POST':
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            errors = {}

            if not firstname:
               errors['firstname'] = 'firstname field is required'
            if not lastname:
               errors['lastname'] = 'lastname field is required'
            if not username:
               errors['username'] = 'username field is required'   
            if User.objects.filter(username=username).exists():
               errors['username'] = 'username is already taken'   
            if not email:
               errors['email'] = 'email field is required'
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
               errors['email'] = 'Invalid email address.'
            if not password:
                errors['password'] = 'password field is required'   
            if password != confirm_password:
                errors['password'] = 'passwords do not match'      
        if errors:
            return JsonResponse(errors, status=400)
        
        User.objects.create_user(
            first_name = firstname,
            last_name = lastname,
            username=username, 
            email=email, 
            password=password
        )

        return JsonResponse({"message": "User created successfully"})
    
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=500)


def editUser(request):

    try:

        if request.method == 'POST':
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            errors = {}

            if not firstname:
               errors['firstname'] = 'firstname field is required'
            if not lastname:
               errors['lastname'] = 'lastname field is required'
            if not username:
               errors['username'] = 'username field is required'   
            if User.objects.filter(username=username).exists():
               errors['username'] = 'username is already taken'   
            if not email:
               errors['email'] = 'email field is required'
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
               errors['email'] = 'Invalid email address.'
            if not password:
                errors['password'] = 'password field is required'   
            if password != confirm_password:
                errors['password'] = 'passwords do not match'      
        if errors:
            return JsonResponse(errors, status=400)
        
        user = User.objects.get(id = id)

        return JsonResponse({"message": "User created successfully"})
    
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=500)
    
   

def deleteGroup(request):
    
    try:
        g_id = request.POST.get('id')
        group = Group.objects.get(id=g_id)
        group.delete()

        return JsonResponse({"message": "Group deleted successfully"})
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=500)    
    