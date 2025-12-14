from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "home/index.html")


def reserve_room(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login') 
    return render(request, "home/reserve.html") 


@login_required(login_url='accounts:login') 
def dashboard(request):
    return render(request, "home/dashboard.html")  
