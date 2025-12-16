from django.shortcuts import render

# Create your views here.
# dashboard/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bookings.models import Reservation
from accounts.forms import CustomUserChangeForm  # فرم ویرایش پروفایل

@login_required
def dashboard(request):
    user = request.user

    # فرم ویرایش پروفایل
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            message = "Profile updated successfully!"
        else:
            message = None
    else:
        form = CustomUserChangeForm(instance=user)
        message = None

    # رزروهای کاربر
    reservations = Reservation.objects.filter(user=user).order_by('-created_at')

    context = {
        "form": form,
        "message": message,
        "reservations": reservations
    }
    return render(request, "dashboard/dashboard.html", context)
