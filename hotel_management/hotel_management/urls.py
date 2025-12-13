"""
URL configuration for hotel_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic.base import TemplateView  # new

from django.contrib.auth.views import LogoutView

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect('/home/')  # اگر می‌خوای صفحه اصلی را render کنی، می‌توانیم template درست کنیم

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('home/')),  # وقتی روت باز شد، به /home/ می‌رود
    path('accounts/', include('accounts.urls')),
    path('home/', include('home.urls')),  # صفحه اصلی را در اپ جداگانه home نگه داریم
]


