from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .forms import ReservationForm
from .models import Reservation, ROOM_CAPACITY, ROOM_PRICE




@login_required(login_url='accounts:login')
def reserve(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            room_type = form.cleaned_data['room_type']
            checkin = form.cleaned_data['checkin_date']
            checkout = form.cleaned_data['checkout_date']

            
            if checkin >= checkout:
                messages.error(request, "Checkout date must be after check-in date.")
            else:
                #if pending reservation is out of time it will be cancelled
                Reservation.objects.filter(
                    room_type=room_type,
                    status="pending",
                    payment_deadline__lt=timezone.now()
                ).update(status="cancelled")

                #count : how many reserve do we have for this date for the roomtype
                booked_count = Reservation.objects.filter(
                    room_type=room_type,
                    status__in=["pending", "paid"],
                    checkin_date__lt=checkout,
                    checkout_date__gt=checkin
                ).count()

                #check room availability
                if booked_count >= ROOM_CAPACITY[room_type]:
                    messages.error(
                        request,
                        f"Sorry, all {room_type} rooms are booked for these dates."
                    )
                else:
                    #we have free room so save
                    reservation = form.save(commit=False)# not yet save in database
                    reservation.user = request.user
                    reservation.is_paid = False
                    reservation.status = "pending"
                    reservation.payment_deadline = timezone.now() + timedelta(minutes=10)
                    reservation.save()

                    
                    messages.success(
                        request,
                        f"Room reserved successfully! Total Price: {reservation.total_price}"
                    )

                    return redirect('bookings:confirm', reservation_id=reservation.id)
    else:# its a Get
        form = ReservationForm()

    return render(request, "bookings/reserve.html", {"form": form})







@login_required(login_url='accounts:login')
# it confirm reserve page
def confirm_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation, id=reservation_id, user=request.user)

    # reserve out of time
    if reservation.is_payment_expired:
        reservation.status = "cancelled"
        reservation.save()
        messages.error(request, "Reservation expired and has been cancelled.")
        return redirect('bookings:dashboard')

    return render(request, "bookings/confirm.html", {"reservation": reservation})


@login_required(login_url='accounts:login')
def pay_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation, id=reservation_id, user=request.user)

    if reservation.is_payment_expired:
        reservation.status = "cancelled"
        reservation.save()
        messages.error(request, "Payment deadline expired. Reservation cancelled.")
    elif not reservation.is_paid:
        reservation.is_paid = True
        reservation.status = "paid"
        reservation.save()
        messages.success(request, "Payment completed successfully!")
    else:
        messages.info(request, "Reservation already paid.")

    return redirect('home:dashboard')


@login_required(login_url='accounts:login')
def dashboard(request):
    # 
    Reservation.objects.filter(
        user=request.user,
        status="pending",
        payment_deadline__lt=timezone.now()
    ).update(status="cancelled")

    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/dashboard.html', {'reservations': reservations})
