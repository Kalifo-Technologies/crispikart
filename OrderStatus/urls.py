from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='orderStatus'),
    path('add', views.addOrderStatus, name='addOrderStatus'),
    path('edit', views.editOrderStatus, name='editOrderStatus'),
    path('delete',views.deleteOrderStatus, name='deleteOrderStatus'),
]