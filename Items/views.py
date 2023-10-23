from django.shortcuts import render, redirect
from Menu.models import Group, Category, Addons, FoodItems, FoodImage, FoodItemGroups, FoodItemCategories, FoodItemAddons
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import JsonResponse


def index(request):

    items_per_page = 10
    foodItems = FoodItems.objects.all()

    paginator = Paginator(foodItems, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    nums = 'a' * page_obj.paginator.num_pages

    foodItemsCount = FoodItems.objects.count()

    context = {
        "nums": nums,
        "page_obj": page_obj,
        "foodItemsCount": foodItemsCount,
        "page_number": page_number
    }
    
    return render(request, 'pages/items/index.html', context)


def addItem(request):

    groups = Group.objects.all()
    categories = Category.objects.all()
    addons = Addons.objects.all()

    if request.method == "POST":
        
            name = request.POST['name']
            price = request.POST['price']
            quantity = request.POST['quantity']
            description  = request.POST['description']
            group = request.POST.getlist('group[]')
            category = request.POST.getlist('category[]')
            addon = request.POST.getlist('addon[]')
            service = request.POST.get('service')
            food_images = request.FILES.getlist('food_images[]')
           

            context = {
                'old_name': name,
                'old_price': price,
                'old_quantity': quantity,
                'old_decription': description,
                'old_group': group,
                'old_category': category,
                'old_addon': addon,
                'old_service': service 
            }
            
            try:
                validation_errors = {}
                if not name:
                    validation_errors['name'] = 'Item name field is required'
                if FoodItems.objects.filter(name=name).exists():
                    validation_errors['name'] = 'Item is already exists with same name'        
                if not quantity:
                    validation_errors['quantity'] = 'Quantity field is required'
                if not price:
                    validation_errors['price'] = 'Price field is required'
                if not service:
                    validation_errors['service'] = 'Service field is required' 

                if validation_errors:
                    return render(request, 'pages/items/create.html', {
                        "groups": groups,
                        "categories": categories,
                        "context": context,
                        "validation_errors": validation_errors
                    })                               

                
                foodItem = FoodItems.objects.create(
                    name = name,
                    price = price,
                    quantity = quantity,
                    description = description,
                    service_type = service
                )

                for value in group:
                    FoodItemGroups.objects.create(
                        foodItems = foodItem,
                        group_id = value
                    )

                for value in category:
                    FoodItemCategories.objects.create(
                        foodItems = foodItem,
                        category_id = value
                    )

                for value in category:
                    FoodItemAddons.objects.create(
                        foodItems = foodItem,
                        addon_id = value
                    )    
    
                for fi in food_images:
                    FoodImage.objects.create(foodItems=foodItem, photo=fi)

                messages.success(request, 'Item saved successfully')

                return redirect('items')
            except ValidationError as e:
                error_message = e.message
                return render(request, 'pages/items/create.html', {"error_message": error_message})
    
    return render(request, 'pages/items/create.html', {'groups':groups,'categories':categories, 'addons': addons})

def editItem(request, id):
    groups = Group.objects.all()
    categories = Category.objects.all()
    addons = Addons.objects.all()
    item = FoodItems.objects.get(id = id)
    firstItemImage = FoodImage.objects.filter(foodItems = id).first()
    item_images = FoodImage.objects.filter(foodItems = id)
    item_images_length = FoodImage.objects.filter(foodItems = id).count()
    selected_groups = FoodItemGroups.objects.filter(foodItems = id)
    selected_categories = FoodItemCategories.objects.filter(foodItems = id) 
    selected_addons = FoodItemAddons.objects.filter(foodItems = id)

    return render(request, 'pages/items/edit.html', 
                  {
                    "groups": groups, 
                    "categories": categories, 
                    "addons": addons,
                    "item": item, 
                    "firstItemImage": firstItemImage, 
                    "item_images": item_images, 
                    "item_images_length": item_images_length,
                    "selected_groups": selected_groups,
                    "selected_categories": selected_categories,
                    "selected_addons": selected_addons 
                  }
                )

def showItem(request, id):
    groups = Group.objects.all()
    categories = Category.objects.all()
    addons = Addons.objects.all()
    item = FoodItems.objects.get(id = id)
    firstItemImage = FoodImage.objects.filter(foodItems = id).first()
    item_images = FoodImage.objects.filter(foodItems = id)
    item_images_length = FoodImage.objects.filter(foodItems = id).count()

    return render(request, 'pages/items/show.html', {"groups": groups, "categories": categories, "addons": addons, "item": item, "firstItemImage": firstItemImage, "item_images": item_images, "item_images_length": item_images_length})

def viewItems(request):

    items_per_page = 15
    foodItems = FoodItems.objects.all()
    
    paginator = Paginator(foodItems, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    nums = 'a' * page_obj.paginator.num_pages

    foodItemsCount = FoodItems.objects.count()

    context = {
        "nums": nums,
        "page_obj": page_obj,
        "foodItemsCount": foodItemsCount,
        "page_number": page_number
    }

    return render(request, 'pages/items/view.html', context)

def updateItem(request, id):

    groups = Group.objects.all()
    categories = Category.objects.all()
    addons = Addons.objects.all()

    if request.method == "POST":
        # Get the existing FoodItems object by its id
        images = FoodImage.objects.filter(foodItems = id)
        name = request.POST['name']
        price = request.POST['price']
        quantity = request.POST['quantity']
        description  = request.POST['description']
        group = request.POST.getlist('group[]')
        category = request.POST.getlist('category[]')
        addon = request.POST.getlist('addon[]')
        service = request.POST.get('service')
        
        editItemImagesField = request.POST.getlist('editItemImagesField[]')

        context = {
            'old_name': name,
            'old_price': price,
            'old_quantity': quantity,
            'old_decription': description,
            'old_group': group,
            'old_category': category,
            'old_addon': addon,
            'old_service': service 
        }
            
        try:
            validation_errors = {}
            if not name:
                validation_errors['name'] = 'Item name field is required'
            if FoodItems.objects.filter(name=name).exclude(id = id).exists():
                validation_errors['name'] = 'Item is already exists with same name'        
            if not quantity:
                validation_errors['quantity'] = 'Quantity field is required'
            if not price:
                validation_errors['price'] = 'Price field is required'
            if not service:
                validation_errors['service'] = 'Service field is required' 

            if validation_errors:
                return render(request, 'pages/items/edit.html', {
                        "groups": groups,
                        "categories": categories,
                        "addons": addons,
                        "context": context,
                        "validation_errors": validation_errors
                })                               

                
            foodItem = FoodItems.objects.get(id = id)
            foodItem.name = name
            foodItem.price = price
            foodItem.quantity = quantity
            foodItem.description = description
            foodItem.service_type = service
            foodItem.save()

            FoodItemGroups.objects.filter(foodItems = foodItem).delete()
            for value in group:
                FoodItemGroups.objects.create(
                    foodItems = foodItem,
                    group_id = value
                )

            FoodItemCategories.objects.filter(foodItems = foodItem).delete()
            for value in category:
                FoodItemCategories.objects.create(
                    foodItems = foodItem,
                    category_id = value
                )

            FoodItemAddons.objects.filter(foodItems = foodItem).delete()
            for value in addon:
                FoodItemAddons.objects.create(
                    foodItems = foodItem,
                    addon_id = value
                )    

            food_images = []
            if 'food_images[]' in request.FILES and request.FILES['food_images[]']:
                if len(images) > 0:
                    for im in images:
                        food_images = request.FILES.getlist('food_images[]', im.photo)

                        FoodImage.objects.filter(foodItems = foodItem).delete()
                        for fi in food_images:
                            FoodImage.objects.create(
                                foodItems=foodItem, 
                                photo=fi
                            )
                else:
                    
                    food_images = request.FILES.getlist('food_images[]')
                    for fi in food_images:
                        FoodImage.objects.create(
                            foodItems=foodItem, 
                            photo=fi
                        )            

            messages.success(request, 'Item updated successfully')

            return redirect('items')
        except ValidationError as e:
                error_message = e.message
                return render(request, 'pages/items/edit.html', {"error_message": error_message})
    
def deleteItem(request):

    delete_id = request.POST.get('id')
    item = FoodItems.objects.get(id = delete_id)
    item.delete()
    return JsonResponse({"message": "Item deleted successfully"})
