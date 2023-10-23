from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='add-ons'),
    path('add', views.storeAddon, name='storeAddon'),
    path('edit', views.editAddon, name='editAddon'),
    path('delete',views.deleteAddon, name='deleteAddon'),
]