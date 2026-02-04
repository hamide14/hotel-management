from django.contrib import admin

# Register your models here.
# bookings/admin.py
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ("user", "room_number", "check_in", "check_out", "status")
#     list_filter = ("status","check_in", "check_out")
#     search_fields = ("user__phone_number", "room_number")
#     raw_id_fields = ("user",)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'check_in', 'check_out', 'room_number')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('user__phone_number', 'user__first_name', 'user__last_name')
    
    
    from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'room_type', 'checkin_date', 'checkout_date', 'guests', 'status', 'is_paid']
    list_filter = ['status', 'room_type', 'is_paid']
    search_fields = ['user__phone_number', 'user__first_name', 'user__last_name']

