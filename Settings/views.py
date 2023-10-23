from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from ProfileSetup.models import PrivateInformation, PublicInformation
import re

# Create your views here.

def accountSettings(request):
    user = User.objects.get(id = request.user.id)
    return render(request, 'pages/settings/index.html', {"user": user})

def updateAccountSettings(request):
    
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        validation_errors = {}
        if not username:
            validation_errors['username'] = 'username field is required' 
        if User.objects.filter(username = username).exclude(username = username).exists():
            validation_errors['username'] = 'username is already exist'       
        if not email:
            validation_errors['email'] = 'email field is required'
        if User.objects.filter(email = email).exclude(email = email).exists():
            validation_errors['email'] = 'email is already exist'    
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            validation_errors['email'] = 'Invalid email address.'  
        if not password:
            validation_errors['password'] = 'password field is required'   
        if password != confirm_password:
            validation_errors['password'] = 'passwords do not match'                
        if validation_errors:
            return render(request, 'pages/settings/index.html', {"validation_errors": validation_errors})
         
        user = User.objects.get(username = request.user.username)    
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.password = password
        user.save()

        messages.success(request, 'Profile saved successfully')
        return redirect('account-settings')  

