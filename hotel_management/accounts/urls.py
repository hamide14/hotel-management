# from django.urls import path
# from .views import signup, signup_done, login_view
# from django.contrib.auth.views import LogoutView
# from django.urls import path
# from . import views

# app_name = "accounts"

# urlpatterns = [
#     path("signup/", signup, name="signup"),
#     path("signup_done/", signup_done, name="signup_done"),
#     path("login/", login_view, name="login"),
#     path("logout/", LogoutView.as_view(next_page='/home/'), name="logout"),
#     path("otp/", views.send_otp, name="send_otp"),
#     path("otp/verify/", views.verify_otp, name="verify_otp"),
    

# ]


from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    # path("signup_done/", views.signup_done, name="signup_done"),  # دیگه لازم نیست
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page='/home/'), name="logout"),
    path("otp/", views.send_otp, name="send_otp"),           
    path("otp/verify/", views.verify_otp, name="verify_otp"), 
]
