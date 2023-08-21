from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):

    user = {'name': User.get_username}

    return render(request, 'pages/dashboard.html', user)