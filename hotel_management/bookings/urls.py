from django.urls import path
from .views import reserve_room, confirm_reservation
from . import views

app_name = "bookings"

urlpatterns = [
    path("reserve/", reserve_room, name="reserve"),
    path("confirm/", confirm_reservation, name="confirm"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('confirm/<int:reservation_id>/',
         views.confirm_reservation, name='confirm'),
    path('pay/<int:reservation_id>/', views.pay_reservation, name='pay')
]
