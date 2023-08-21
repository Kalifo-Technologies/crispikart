from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='groups'),
    path('add', views.addGroup, name='addGroup'),
    path('edit', views.editGroup, name='editGroup'),
    path('delete',views.deleteGroup, name='deleteGroup'),
]