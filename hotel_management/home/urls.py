
from django.urls import path
from . import views

app_name = "home"  

urlpatterns = [
    path('', views.index, name='home'),
    path('reserve/', views.reserve_room, name='reserve'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
