from django.urls import path
from . import views

urlpatterns = [
    path('group-list', views.groupList, name='group-list'),
    path('group-add', views.groupStore, name='group-add'),
    path('group-edit/<int:id>', views.groupEdit, name='group-edit'),
    path('group-update/<int:id>', views.groupUpdate, name='group-update'),
    path('group-delete/<int:id>', views.groupDelete, name='group-delete'),

    path('category-list', views.categoryList, name='category-list'),
    path('category-add', views.categoryStore, name='category-add'),
    path('category-edit/<int:id>', views.categoryEdit, name='category-edit'),
    path('category-update/<int:id>', views.categoryUpdate, name='category-update'),
    path('category-delete/<int:id>', views.categoryDelete, name='category-delete'),
    
]
