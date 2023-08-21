from django.shortcuts import render, redirect
from Menu.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import datetime
from django.core.exceptions import ValidationError
from django.http import JsonResponse
# Create your views here.

def index(request):

    groups_list = Group.objects.all()
    page = request.GET.get('page')
    groups = Paginator(groups_list, 10)
    
    s = groups.get_page(page)
    nums = 'a' * s.paginator.num_pages
    
    groupsCount = Group.objects.count()

    return render(request, 'pages/groups/index.html', {"groups": s,'nums':nums, "groupsCount": groupsCount})

def addGroup(request):

    if request.method == "POST":
        req = request.POST
        name = req.get('name')
        start_time = req.get('StartTime')
        end_time = req.get('EndTime')
    try:

        errors = {}
        if not name:
            errors['name'] = 'Group name field is required'
        if Group.objects.filter(name=name).exists():
            errors['name'] = 'Group already exists with same name'      
        if errors:
            return JsonResponse(errors, status=400)
        
        Group.objects.create(
             name=name,
             StartTime=start_time,
             EndTime=end_time
        )
        return JsonResponse({"message": "Group created successfully"})
    
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=500)

    
def editGroup(request):

    name = request.POST.get('name')
    g_id = request.POST.get('id')
    start_time = request.POST.get('StartTime')
    end_time = request.POST.get('EndTime')

    try:
        errors = {}
        
        if not name:
            errors['name'] = 'Group name field is required'
        if Group.objects.exclude(id = g_id).filter(name=name).exists():
            errors['name'] = 'Group already exists with same name'
        if errors:
            return JsonResponse(errors, status=400)

        group = Group.objects.get(id=g_id)
        group.name = name
        group.StartTime = start_time
        group.EndTime = end_time
        group.save()

        return JsonResponse({"message": "Group updated successfully"})
    
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
    