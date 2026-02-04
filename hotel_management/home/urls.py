from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.home, name='home'),
    #run function views.dashboard when url is dashboard
    path('dashboard/', views.dashboard , name='dashboard'),
]
