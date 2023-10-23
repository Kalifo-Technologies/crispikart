from django.urls import path
from . import views

urlpatterns = [
    path('account-settings', views.accountSettings, name='account-settings'),
    path('update-account-settings', views.updateAccountSettings, name='update-account-settings')
]