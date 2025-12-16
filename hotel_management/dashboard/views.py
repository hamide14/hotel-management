from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bookings.models import Reservation
from accounts.forms import CustomUserChangeForm


@login_required
def dashboard(request):
    user = request.user

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)  #change informations in dashboard
        if form.is_valid():
            form.save()
            message = "Profile updated successfully!"
        else:
            message = None
    else:
        form = CustomUserChangeForm(instance=user) # current informations will show in form 
        message = None

    reservations = Reservation.objects.filter(
        user=user).order_by('-created_at')    #reserves will be shown from old to new

    context = {
        "form": form,
        "message": message,
        "reservations": reservations
    }
    return render(request, "dashboard/dashboard.html", context)
