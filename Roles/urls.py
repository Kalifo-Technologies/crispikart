from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='roles'),
    path('add', views.addRole, name='addRole'),
    path('edit', views.editRole, name='editRole'),
    path('delete',views.deleteRole, name='deleteRole'),
]