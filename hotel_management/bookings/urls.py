from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("reserve/", views.reserve, name="reserve"),
    path("confirm/<int:reservation_id>/", views.confirm_reservation, name="confirm"),
    path("pay/<int:reservation_id>/", views.pay_reservation, name="pay"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
