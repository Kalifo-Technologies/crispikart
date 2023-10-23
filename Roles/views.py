from django.shortcuts import render, redirect
from User.models import Roles
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.exceptions import ValidationError
# Create your views here.

def index(request):

    roles = Roles.objects.all()
    paginator = Paginator(roles, 10)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    nums = 'a' * page.paginator.num_pages

    rolesCount = Roles.objects.count()

    return render(request, 'pages/roles/index.html', {"rolesCount": rolesCount, "roles": page, "nums": nums})

def addRole(request):

    if request.method == "POST":        
        req = request.POST
        try:
            name_field = req.get('name', '').strip()
            errors = {}
            if not name_field:
                errors['name'] = 'Role name field is required'
            if Roles.objects.filter(name=name_field).exists():
                errors['name'] = 'Role is already exists with same name'
            if errors:
                return JsonResponse(errors, status=400)    
            
            Roles.objects.create(name=name_field)        
            return JsonResponse({"message": "Role created successfully"})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=500)

    
def editRole(request):

    req = request.POST
    edit_id = request.POST.get('id')

    try:
        name_field = req.get('name', '').strip()
        errors = {}
        if not name_field:
            errors['name'] = 'Role name field is required'
        if Roles.objects.exclude(id = edit_id).filter(name = name_field).exists():
            errors['name'] = 'Role is already exists with same name'
        if errors:
            return JsonResponse(errors, status=400)    

        role = Roles.objects.get(id=edit_id)
        role.name = name_field
        role.save()
        return JsonResponse({"message": "Role updated successfully"})
    except ValidationError as e:    
         return JsonResponse({'error': str(e)}, status=500)
    

def deleteRole(request):
    
    delete_id = request.POST.get('id')
    role = Roles.objects.get(id=delete_id)
    role.delete()
    
    return JsonResponse({"message": "Role deleted successfully"})





