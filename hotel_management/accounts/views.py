from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random
from django.conf import settings
from .models import EmailOTP
from .forms import EmailForm, OTPForm

#what do we get when we click on any url


def signup(request):
    if request.method == "POST":
        #create user form from customusercreadtionform  and put data in it
        form = CustomUserCreationForm(request.POST)
        # we validate data 
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            code = str(random.randint(100000, 999999))
            EmailOTP.objects.create(user=user, code=code)

            send_mail(
                "Your Signup OTP",
                f"Your OTP code is: {code}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )

            request.session["otp_user_id"] = user.id #save user uid in session
            return redirect("accounts:verify_otp")
    else:# its Get so empty form there
        form = CustomUserCreationForm()
        
    #context render and form goes to context
    return render(request, "signup/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated: #if already loging no need again
        return redirect("home:home")

    if request.method == "POST":
        form = LoginForm(request.POST) #create a login form wiht phone and pass
        if form.is_valid():
            # get validated data from form
            phone = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]

            #check if there is any user wiht this info 
            user = authenticate(request, username=phone, password=password)
            #authenticate return user object or none
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect("home:home")
                else:
                    request.session["otp_user_id"] = user.id
                    return redirect("accounts:verify_otp")
            else:
                messages.error(request, "Phone number or password is incorrect")
                return render(request, "login/login.html", {"form": form}) #try again
    else: #if its get just empty form 
        form = LoginForm()
        
    return render(request, "login/login.html", {"form": form})


User = get_user_model()


def send_otp(request):
    if request.method == "POST":#if its post user sent their email 
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            
            user = User.objects.filter(email=email).first()
            if not user:
                return render(request, "OTP/send_otp.html", {
                    "form": form,
                    "error": "User not found"
                })

            EmailOTP.objects.filter(user=user).delete()
            
            code = str(random.randint(100000, 999999))
            EmailOTP.objects.create(user=user, code=code)

            send_mail(
                "Your Login Code",
                f"Your OTP code is: {code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )

            request.session["otp_user_id"] = user.id
            return redirect("accounts:verify_otp")
    else:#its a Get (empy form for email)
        form = EmailForm()

    return render(request, "OTP/send_otp.html", {"form": form})


def verify_otp(request):
    user_id = request.session.get("otp_user_id")
    if not user_id:# session gone or not set
        return redirect("accounts:send_otp")

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]

            otp = EmailOTP.objects.filter(
                user_id=user_id,
                code=code
            ).order_by("-created_at").first()

            if otp and otp.is_valid():
                user = otp.user
                user.is_active = True
                user.save()
                login(request, user)
                otp.delete()
                request.session.pop("otp_user_id", None)
                return redirect("home:home")
            else:
                messages.error(request, "Invalid or expired code")
    else:#its a get
        form = OTPForm()

    return render(request, "OTP/verify_otp.html", {"form": form})
