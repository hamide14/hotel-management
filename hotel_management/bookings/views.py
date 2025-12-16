from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReservationForm
from .models import Reservation
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation
from rooms.models import RoomType
from django.utils import timezone

@login_required(login_url='accounts:login')
def reserve_room(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            room_type = form.cleaned_data['room_type']
            checkin = form.cleaned_data['checkin_date']
            checkout = form.cleaned_data['checkout_date']

            # تعداد رزروهای موجود در همان بازه
            booked_count = Reservation.objects.filter(
                room_type=room_type,
                checkin_date__lt=checkout,
                checkout_date__gt=checkin
            ).count()

            if booked_count >= room_type.capacity:
                messages.error(request, f"Sorry, all {room_type.name} rooms are booked for these dates.")
            else:
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.save()
                return redirect('bookings:confirm')
    else:
        form = ReservationForm()

    return render(request, "bookings/reserve.html", {"form": form})

@login_required(login_url='accounts:login')
def confirm_reservation(request):
    return render(request, "bookings/confirm.html")



def reserve_room(request):
    if request.method == "POST":
        room_type_id = request.POST.get("room_type")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        room_type = RoomType.objects.get(id=room_type_id)

        # تعداد رزروهای موجود برای همان تاریخ
        existing_bookings = Booking.objects.filter(
            room_type=room_type,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).count()

        if existing_bookings >= room_type.capacity:
            messages.error(request, f"Sorry, no {room_type.name} rooms available for these dates.")
            return redirect("home:reserve")

        # ذخیره رزرو
        Booking.objects.create(
            user=request.user,
            room_type=room_type,
            check_in=check_in,
            check_out=check_out,
            status="pending"
        )

        messages.success(request, "Room reserved successfully!")
        return redirect("home:reserve")

    # GET
    room_types = RoomType.objects.all()
    return render(request, "bookings/reserve.html", {"room_types": room_types})