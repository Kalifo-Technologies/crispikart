from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='users'),
    path('add', views.addUser, name='addUser'),
    path('edit', views.editUser, name='editUser'),
    path('delete', views.deleteUser, name='deleteUser')
]

