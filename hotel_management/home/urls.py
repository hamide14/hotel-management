
from django.urls import path
from . import views

app_name = "home"  

urlpatterns = [
    path('', views.home, name='home'),
    path('reserve/', views.reserve, name='reserve'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
