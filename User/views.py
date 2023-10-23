from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from User.models import Roles
import re

def index(request):

    items_per_page = 10
    roles = Roles.objects.all()
    users = User.objects.all()
    paginator = Paginator(users, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    nums = 'a' * page_obj.paginator.num_pages

    usersCount = User.objects.count()

    context = {
        "roles": roles,
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
            role = request.POST['role']
            is_active = request.POST.get('is_active')
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            errors = {}

            if not firstname:
               errors['first_name'] = 'firstname field is required'
            if not lastname:
               errors['last_name'] = 'lastname field is required'
            if not username:
               errors['username'] = 'username field is required'   
            if User.objects.filter(username=username).exists():
               errors['username'] = 'username is already taken'   
            if not email:
               errors['email'] = 'email field is required'
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
               errors['email'] = 'Invalid email address.'
            if not role:
                errors['role'] = 'role field is required'   
            if not password:
                errors['password'] = 'password field is required'   
            if password != confirm_password:
                errors['password'] = 'passwords do not match'      
        if errors:
            return JsonResponse(errors, status=400)
        
        user = User.objects.create_user(
            first_name = firstname,
            last_name = lastname,
            username = username, 
            email = email, 
            is_active = is_active,
            password = password
        )

        Group.objects.create(
            user_id = user,
            group_id = role
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
            role = request.POST.get('role')
            is_active = request.POST.get('is_active')
            edit_id = request.POST['edit_id']

            errors = {}

            if not firstname:
               errors['first_name'] = 'firstname field is required'
            if not lastname:
               errors['last_name'] = 'lastname field is required'
            if not username:
               errors['username'] = 'username field is required'   
            if User.objects.filter(username=username).exclude(id = edit_id).exists():
               errors['username'] = 'username is already taken'   
            if not email:
               errors['email'] = 'email field is required'
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
               errors['email'] = 'Invalid email address.'
            if not role:
               errors['role'] = 'role field is required'

        if errors:
            return JsonResponse(errors, status=400)
        
        user = User.objects.get(id = edit_id)
        user.first_name =  firstname
        user.last_name = lastname
        user.username = username
        user.email = email
        user.is_active = is_active
        user.save()

        group = Group.objects.get(user_id = user)
        group.group_id = role
        group.save()

        return JsonResponse({"message": "User updated successfully"})
    
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=500)
    
   

def deleteUser(request):
    
    try:
        delete_id = request.POST.get('delete_id')
        user = User.objects.get(id=delete_id)
        user.delete()

        return JsonResponse({"message": "User deleted successfully"})
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=500)    
    