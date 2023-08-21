from django.urls import path
from Orders.views import *

urlpatterns = [
    path('list/',list_orders,name = 'list-orders'),
    path('delete/',delete_order,name='delete-order'),
]