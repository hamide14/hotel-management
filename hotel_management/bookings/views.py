from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import ReservationForm
from .models import Reservation
from rooms.models import RoomType


@login_required(login_url='accounts:login')
def reserve(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            room_type = form.cleaned_data['room_type']
            checkin = form.cleaned_data['checkin_date']
            checkout = form.cleaned_data['checkout_date']
            if checkin >= checkout:
                messages.error(
                    request,
                    "Checkout date must be after check-in date."
                )
            else:
                expired_reservations = Reservation.objects.filter(
                    room_type=room_type,
                    status="pending",
                    payment_deadline__lt=timezone.now()
                )
                for res in expired_reservations:
                    res.status = "cancelled"
                    res.save()
                booked_count = Reservation.objects.filter(
                    room_type=room_type,
                    status="pending",
                    checkin_date__lt=checkout,
                    checkout_date__gt=checkin
                ).count()
                if booked_count >= room_type.rooms:
                    messages.error(
                        request,
                        f"Sorry, all {room_type.name} rooms are booked for these dates."
                    )
                else:
                    reservation = form.save(commit=False)
                    reservation.user = request.user
                    reservation.is_paid = False
                    reservation.status = "pending"
                    reservation.payment_deadline = timezone.now() + timedelta(minutes=10)
                    reservation.save()
                    messages.success(
                        request,
                        "Room reserved successfully! You have 10 minutes to complete the payment."
                    )
                    return redirect('bookings:confirm', reservation_id=reservation.id)
    else:
        form = ReservationForm()
    return render(
        request,
        "bookings/reserve.html",
        {"form": form}
    )


@login_required(login_url='accounts:login')
def confirm_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation, id=reservation_id, user=request.user)

    if reservation.is_payment_expired:
        reservation.status = "cancelled"
        reservation.save()
        messages.error(request, "Reservation expired and has been cancelled.")
        return redirect('bookings:dashboard')
    return render(
        request,
        "bookings/confirm.html",
        {"reservation": reservation}
    )


@login_required(login_url='accounts:login')
def pay_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation, id=reservation_id, user=request.user)
    if reservation.is_payment_expired:
        reservation.status = "cancelled"
        reservation.save()
        messages.error(
            request, "Payment deadline expired. Reservation cancelled.")
    elif not reservation.is_paid:
        reservation.is_paid = True
        reservation.status = "paid"
        reservation.save()
        messages.success(request, "Payment completed successfully!")
    else:
        messages.info(request, "Reservation already paid.")

    return redirect('bookings:dashboard')


@login_required(login_url='accounts:login')
def dashboard(request):
    pending_expired = Reservation.objects.filter(
        user=request.user,
        status="pending",
        payment_deadline__lt=timezone.now()
    )
    for res in pending_expired:
        res.status = "cancelled"
        res.save()
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'dashboard/dashboard.html', {'reservations': reservations})
