from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signup_done/", views.signup_done, name="signup_done"),
    path("login/", views.user_login, name="login"),  # مسیر لاگین
]
