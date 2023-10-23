from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def index(request):

    if request.user.is_authenticated == True:
        user = {'name': User.get_username}
        return render(request, 'pages/dashboard.html', user)
    else:    
        return redirect('login')

