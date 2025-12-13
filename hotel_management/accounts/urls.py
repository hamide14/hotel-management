# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.register_page, name='signin'),
    path('signin-done/', views.signin_done, name='signin_done'),
    path('login/', views.login_page, name='login'),
]
