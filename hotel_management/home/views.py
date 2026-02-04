from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from bookings.models import Reservation
from accounts.forms import CustomUserChangeForm
#render for showing html pages


#path('', views.home, name='home')
def home(request):
    # when user goes to /
    return render(request, "home/home.html")







@login_required(login_url='accounts:login') #only logged in users can see dashboard if not redirect to login page

#path('dashboard/', views.dashboard , name='dashboard')
def dashboard(request):
    user = request.user
    #take user form request

    if request.method == "POST":
        #create form for edit user info
        form = CustomUserChangeForm(request.POST, instance=user) # form will be filled
        if form.is_valid():# are the info valid?
            form.save()
            message = "Profile updated successfully!"
        else:
            message = None
    else:
        # if user just open the dashboard mean its get and only form will filled with info
        form = CustomUserChangeForm(instance=user)
        message = None
        
        
        
    # take all current reservation from reservaion model
    #and sort by newest first
    reservations = Reservation.objects.filter(
        user=user
    ).order_by('-created_at')
     
    # needed info for showing in dashboard
    context = {
        "form": form,
        "message": message,
        "reservations": reservations
    }
    #send context to dashboard html page

    return render(request, "dashboard/dashboard.html", context)
