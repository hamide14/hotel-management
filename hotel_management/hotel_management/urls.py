from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # lambda take the function and redirect to home
    path('', lambda request: redirect('home/')), # if we go to base localhost it will redirect to home 
    path('accounts/', include('accounts.urls')),# every urls about account login and signup 
    path('home/', include('home.urls')), # likewise for home app
    path('bookings/', include('bookings.urls')),  # likewise for booking app  
    

]
