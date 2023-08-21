from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.sign_up, name='sign-up'),
    path('login', views.sign_in, name='sign-in'),
    path('logout', views.signout, name='sign-out')
]
