from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login




def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("accounts:signup_done")
        else:
       
            print("Form errors:", form.errors)  
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")

    else:
        form = CustomUserCreationForm()

    return render(request, "signup/signup.html", {"form": form})



def signup_done(request):
    return render(request, "signup/signup_done.html")





def login_view(request):
    if request.user.is_authenticated:
        return redirect("home:home") 

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=phone,  
                password=password
            )

            if user:
                login(request, user)
                return redirect("home:home")  
            else:
                messages.error(request, "Phone number or password is incorrect")
    else:
        form = LoginForm()

    return render(request, "login/login.html", {"form": form})

