from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='items'),
    path('add', views.addItem, name='addItem'),
    path('view', views.viewItems, name='viewItems'),
    path('show/<int:id>', views.showItem, name='showItem'),
    path('edit/<int:id>', views.editItem, name='editItem'),
    path('delete', views.deleteItem, name="deleteItem"),
    path('update/<int:id>', views.updateItem, name="updateItem")
]