from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='delivary-boys'),
    path('add', views.addDelivaryBoy, name='addDelivaryBoy'),
    path('edit', views.editDelivaryBoy, name='editDelivaryBoy'),
    path('delete', views.deleteDelivaryBoy, name='deleteDelivaryBoy'),
]
