"""
URL configuration for Restorant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('auth/', include('Auth.urls')),
    path('dashboard/', include('Dashboard.urls')),
    path('groups/', include('Groups.urls')),
    path('categories/', include('Category.urls')),
    path('add-ons/', include('Addons.urls')),
    path('items/', include('Items.urls')),
    path('order-status/', include('OrderStatus.urls')),
    path('profiles/', include('ProfileSetup.urls')),
    path('delivary-boys/', include('DelivaryBoys.urls')),
    path('users/', include('User.urls')),
    path('roles/', include('Roles.urls')),
    path('settings/', include('Settings.urls')),
    path('api/', include('api.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
