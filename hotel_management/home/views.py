from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    #when user goes to home/
    return render(request, "home/home.html")

#request.user.is_authenticated
@login_required(login_url='accounts:login')
def reserve(request):
        return render(request, "bookings/reserve.html")  
   

@login_required(login_url='accounts:login')
def dashboard(request):
    return render(request, "dashboard/dashboard.html")
