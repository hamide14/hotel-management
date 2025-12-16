from django.urls import path
from .views import reserve_room, confirm_reservation

app_name = "bookings"

urlpatterns = [
    path("reserve/", reserve_room, name="reserve"),
    path("confirm/", confirm_reservation, name="confirm"),
]
