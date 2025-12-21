from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('home/')), 
    path('accounts/', include('accounts.urls')),
    path('home/', include('home.urls')),
    path('bookings/', include('bookings.urls')),   
    

]
