from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

def sign_up(request):
    return render(request, 'auth/signup.html')

def register(request):

    try:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            context = {
                "old_username": username,
                "old_email": email 
            }
        
            validation_errors = {}
            if not username:
                validation_errors['username'] = 'username field is required' 
            if User.objects.filter(username = username).exists():
                validation_errors['username'] = 'username is already exist'       
            if not email:
                validation_errors['email'] = 'email field is required'
            if User.objects.filter(email = email).exists():
                validation_errors['email'] = 'email is already exist'    
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                validation_errors['email'] = 'Invalid email address.'  
            if not password:
                validation_errors['password'] = 'password field is required'   
            if password != confirm_password:
                validation_errors['password'] = 'passwords do not match'                
            if validation_errors:
                return render(request, 'auth/signup.html', {"validation_errors": validation_errors, "context": context})

        User.objects.create_superuser(
            email = email,
            username = username,
            password = password
        )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            messages.success(request, 'Registration Successful')
            return redirect('dashboard')
    
    except ValidationError as e:
            error_message = e.message
            return render(request, 'auth/signup.html', {"error_message": error_message})  

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'incorrect username or password')
            return redirect('sign-in')
    return render(request,'auth/login.html')

@login_required
def signout(request):
    logout(request)
    return redirect('sign-in')

    


