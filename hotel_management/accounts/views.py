from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import EmailOTP
from .forms import EmailForm, OTPForm


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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

            user = authenticate(request, username=phone, password=password)
            if user:
                # return user object
                login(request, user)  # session
                return redirect("home:home")
            # else:
                # return None
                # messages.error(
                #     request, "Phone number or password is incorrect")
    else:
        form = LoginForm()

    return render(request, "login/login.html", {"form": form})


User = get_user_model()


def send_otp(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            user = User.objects.filter(email=email).first()
            if not user:
                return render(request, "OTP/send_otp.html", {
                    "form": form,
                    "error": "User not found"
                })

            code = str(random.randint(100000, 999999))
            EmailOTP.objects.create(user=user, code=code)

            send_mail(
                "Your Login Code",
                f"Your OTP code is: {code}",
                "noreply@hotel.com",
                [email]
            )

            request.session["otp_user_id"] = user.id
            return redirect("accounts:verify_otp")
    else:
        form = EmailForm()

    return render(request, "OTP/send_otp.html", {"form": form})


def verify_otp(request):
    user_id = request.session.get("otp_user_id")
    if not user_id:
        return redirect("accounts:send_otp")

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]

            print("user_id:", user_id)
            print("code entered:", code)

            otp = EmailOTP.objects.filter(
                user_id=user_id,
                code=code
            ).order_by("-created_at").first()

            print("otp found:", otp)

            if otp and otp.is_valid():
                login(request, otp.user)
                otp.delete()
                return redirect("home:home")
            else:
                return render(request, "OTP/verify_otp.html", {
                    "form": form,
                    "error": "Invalid or expired code"
                })
    else:
        form = OTPForm()

    return render(request, "OTP/verify_otp.html", {"form": form})
