from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='categories'),
    path('add', views.addCategory, name='addCategory'),
    path('edit', views.editCategory, name='editCategory'),
    path('delete', views.deleteCategory, name='deleteCategory'),

]
