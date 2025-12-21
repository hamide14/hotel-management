from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from bookings.models import Reservation
from accounts.forms import CustomUserChangeForm


def home(request):
    # when user goes to /
    return render(request, "home/home.html")




@login_required(login_url='accounts:login')
def dashboard(request):
    user = request.user

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

    reservations = Reservation.objects.filter(
        user=user
    ).order_by('-created_at')

    context = {
        "form": form,
        "message": message,
        "reservations": reservations
    }

    return render(request, "dashboard/dashboard.html", context)
