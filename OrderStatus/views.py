from django.shortcuts import render, redirect
from Menu.models import OrderStatus
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.exceptions import ValidationError
# Create your views here.

def index(request):

    order_status = OrderStatus.objects.all()
    paginator = Paginator(order_status, 10)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    nums = 'a' * page.paginator.num_pages

    orderStatusCount = OrderStatus.objects.count()

    return render(request, 'pages/order_status/index.html', {"orderStatusCount": orderStatusCount, "orderStatus": page, "nums": nums})

def addOrderStatus(request):

    if request.method == "POST":        
        req = request.POST
        try:
            name_field = req.get('name', '').strip()
            errors = {}
            if not name_field:
                errors['name'] = 'Order Status name field is required'
            if OrderStatus.objects.filter(name=name_field).exists():
                errors['name'] = 'Order Status is already exists with same name'
            if errors:
                return JsonResponse(errors, status=400)    
            OrderStatus.objects.create(name=name_field)        
            return JsonResponse({"message": "Order Status created successfully"})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=500)

    
def editOrderStatus(request):

    req = request.POST
    edit_id = request.POST.get('id')

    try:
        name_field = req.get('name', '').strip()
        errors = {}
        if not name_field:
            errors['name'] = 'Order Status name field is required'
        if OrderStatus.objects.exclude(id = edit_id).filter(name = name_field).exists():
            errors['name'] = 'Order Status is already exists with same name'
        if errors:
            return JsonResponse(errors, status=400)    

        orderStatus = OrderStatus.objects.get(id=edit_id)
        orderStatus.name = name_field
        orderStatus.save()
        return JsonResponse({"message": "Order Status updated successfully"})
    except ValidationError as e:    
         return JsonResponse({'error': str(e)}, status=500)
    

def deleteOrderStatus(request):
    
    delete_id = request.POST.get('id')
    orderStatus = OrderStatus.objects.get(id=delete_id)
    orderStatus.delete()
    
    return JsonResponse({"message": "Order Status deleted successfully"})





