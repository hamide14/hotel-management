from django.urls import path
from .views import signup, signup_done, login_view
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signup_done/", signup_done, name="signup_done"),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page='/home/'), name="logout"),
]
