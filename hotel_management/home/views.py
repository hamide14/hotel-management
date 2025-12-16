from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def index(request):
    #when user goes to home/
    return render(request, "home/index.html")

#request.user.is_authenticated
@login_required(login_url='accounts:login')
def reserve_room(request):
        return render(request, "home/reserve.html")  
   

@login_required(login_url='accounts:login')
def dashboard(request):
    return render(request, "home/dashboard.html")
