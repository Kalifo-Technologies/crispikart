from django.shortcuts import render, redirect
from django.contrib import messages
from Menu.models import Category, Group, Addons
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def index(request):
    
    items_per_page = 10
    
    addons = Addons.objects.all()
    paginator = Paginator(addons, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    nums = 'a' * page_obj.paginator.num_pages

    addonsCount =   Addons.objects.count()

    context = {
        "addons": addons,
        "nums": nums,
        "page_obj": page_obj,
        "addonsCount": addonsCount,
        "page_number": page_number
    }
    
    return render(request, 'pages/addons/index.html', context)

def storeAddon(request):

        try:
            if request.method == "POST":

                req = request.POST

                name = req.get('name')
                photo = request.FILES.get('photo')

                errors = {}

                if not name:
                    errors['name'] = 'name field is required'
                if Addons.objects.filter(name=name).exists():
                    errors['name'] = 'Addon is already exists with same name'
                if errors:
                    return JsonResponse(errors, status=400)        
                
                Addons.objects.create(
                    name = name,
                    photo = photo
                )

                return JsonResponse({"message": "Addon created successfully"}, status=200)
            
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=500)
            
        
    
def editAddon(request):

    try:    
        if request.method == "POST":
            req = request.POST
            name = req.get('name')
            edit_id = req.get('id')

            errors = {}

            if not name:
                errors['name'] = 'name field is required'
            if Addons.objects.exclude(id = edit_id).filter(name=name).exists():
                errors['name'] = 'Addon is already exists with same name'
            if errors:
                return JsonResponse(errors, status=400)        

            addon = Addons.objects.get(id = edit_id)
            image = request.FILES.get('photo', addon.photo)
            addon.name = name
            addon.photo = image    
            addon.save()

            return JsonResponse({"message": "Addon updated successfully"})
            
    except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=500)    
    

def deleteAddon(request):
    delete_id = request.POST.get('id')
    addon = Addons.objects.get(id = delete_id)
    addon.delete()
    
    return JsonResponse({"message": "Addon deleted successfully"})


        
