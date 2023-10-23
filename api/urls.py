from django.urls import path
from . import views
from django.urls import path
from .views import send_otp, verify_otp
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    
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

    path('addon-list', views.addonList, name='addon-list'),
    path('addon-add', views.addonStore, name='addon-add'),
    path('addon-edit/<int:id>', views.addonEdit, name='addon-edit'),
    path('addon-update/<int:id>', views.addonUpdate, name='addon-update'),
    path('addon-delete/<int:id>', views.addonDelete, name='addon-delete'),
    
    path('order-status-list', views.orderStatusList, name='order-status-list'),
    path('order-status-add', views.orderStatusStore, name='order-status-add'),
    path('order-status-edit/<int:id>', views.orderStatusEdit, name='order-status-edit'),
    path('order-status-update/<int:id>', views.orderStatusUpdate, name='order-status-update'),
    path('order-status-delete/<int:id>', views.orderStatusDelete, name='order-status-delete'),

    path('food-item-list', views.foodItemsList, name='food-item-list'),
    path('food-item-add', views.foodItemStore, name='food-item-add'),
    path('food-item-edit/<int:id>', views.foodItemEdit, name='food-item-edit'),
    path('food-item-update/<int:id>', views.foodItemUpdate, name='food-item-update'),
    path('food-item-delete/<int:id>', views.foodItemDelete, name='food-item-delete'),

    path('profile-list', views.profileList, name='profile-list'),
    path('add-profile', views.profileStore, name='add-profile'),
    path('edit-profile/<int:id>', views.profileEdit, name='edit-profile'),
    path('update-profile/<int:id>', views.profileUpdate, name='update-profile'),
    path('delete-profile/<int:id>', views.profileDelete, name='delete-profile'),
]
