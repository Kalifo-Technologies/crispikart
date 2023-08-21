from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='profiles'),
    path('create', views.create, name='create'),
    path('add', views.addProfile, name='addProfile'),
    path('edit/<int:id>/', views.editProfile, name='editProfile'),
    path('update/<int:id>/', views.updateProfile, name='updateProfile'),
    path('delete', views.deleteProfile, name='deleteProfile')
]