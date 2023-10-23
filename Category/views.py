from django.shortcuts import render, redirect
from django.contrib import messages
from Menu.models import Category, Group
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def index(request):
    
    items_per_page = 10
    categories = Category.objects.all()
    groups = Group.objects.all()
    paginator = Paginator(categories, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    nums = 'a' * page_obj.paginator.num_pages

    categoriesCount = Category.objects.count()

    context = {
        "groups": groups,
        "nums": nums,
        "page_obj": page_obj,
        "categoriesCount": categoriesCount,
        "page_number": page_number
    }
    
    return render(request, 'pages/categories/index.html', context)

def addCategory(request):

        try:
            if request.method == "POST":

                req = request.POST

                name = req.get('name')
                group_id = req.get('group_id')
                image = request.FILES.get('image')

                errors = {}

                if not name:
                    errors['name'] = 'Category name field is required'
                if not group_id:
                    errors['group_id'] = 'Group field is required'
                if Category.objects.filter(name=name).exists():
                    errors['name'] = 'Category is already exists with same name'
                if errors:
                    return JsonResponse(errors, status=400)        
                
                Category.objects.create(
                    group_id = group_id,
                    name = name,
                    image = image
                )

                return JsonResponse({"message": "Category created successfully"}, status=200)
            
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=500)
            
        
    
def editCategory(request):

    try:    
        if request.method == "POST":
            req = request.POST
            name = req.get('name')
            group_id = req.get('group_id')
            edit_id = req.get('edit_id')

            errors = {}

            if not name:
                errors['name'] = 'Category name field is required'
            if not group_id:
                errors['group_id'] = 'Group field is required'
            if Category.objects.exclude(id = edit_id).filter(name=name).exists():
                errors['name'] = 'Category is already exists with same name'
            if errors:
                return JsonResponse(errors, status=400)        

            category = Category.objects.get(id = edit_id)
            image = request.FILES.get('image', category.image)
            category.name = name
            category.group_id = group_id
            category.image = image    
            category.save()
            return JsonResponse({"message": "Category updated successfully"})
            
    except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=500)    
    

def deleteCategory(request):
    delete_id = request.POST.get('delete_id')
    group = Category.objects.get(id = delete_id)
    group.delete()
    
    return JsonResponse({"message": "Category deleted successfully"})


        
