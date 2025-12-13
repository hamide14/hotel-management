from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("signup_done")
        else:
            print(form.errors)  # نمایش خطاهای فرم برای debug
    else:
        form = CustomUserCreationForm()
    return render(request, "signup/signup.html", {"form": form})


def signup_done(request):
    return render(request, "signup/signup_done.html")


def user_login(request):
    pass