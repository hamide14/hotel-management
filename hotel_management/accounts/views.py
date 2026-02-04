from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import EmailOTP
from .forms import EmailForm, OTPForm


def signup(request):
    if request.method == "POST":
        #create login form from customusercreadtionform  and put data in it
        form = CustomUserCreationForm(request.POST)
        # we validate data 
        if form.is_valid():
            form.save() #save in customeruser model and go to done page
            return redirect("accounts:signup_done")
    else:# its Get so empty form there
        form = CustomUserCreationForm()
        
    #context render and form goes to context
    return render(request, "signup/signup.html", {"form": form})


def signup_done(request):
    return render(request, "signup/signup_done.html")



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
                login(request, user)
                return redirect("home:home")
            else:
                
                messages.error(request, "Phone number or password is incorrect")
                #render form again for try again
                return render(request, "login/login.html", {"form": form})
    else: #if its get just empty form 
        form = LoginForm()
        
    # render template (create html page and send to browser)
    # we got url of template and we send our forms to it also errors
    return render(request, "login/login.html", {"form": form})


User = get_user_model()


def send_otp(request):
    if request.method == "POST":#if its post user sent their email 
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            
            # do we have user with this email?
            user = User.objects.filter(email=email).first()# no? none
            #if not show the send otp form agina and user not found
            if not user:
                return render(request, "OTP/send_otp.html", {
                    "form": form,
                    "error": "User not found"
                })

            #delete old otps for this user 
            EmailOTP.objects.filter(user=user).delete()
            
            #random 6 digite code

            code = str(random.randint(100000, 999999))
            
            EmailOTP.objects.create(user=user, code=code)
            # function for sending email
            send_mail(
                "Your Login Code",                # subject
    f"Your OTP code is: {code}",     # message
    settings.DEFAULT_FROM_EMAIL,      # from_email
    [email],                          # recipient_list
    fail_silently=False
            )

            request.session["otp_user_id"] = user.id #store user id in session for later use
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

            if otp and otp.is_valid() and otp.user.is_active:
                login(request, otp.user)
                otp.delete()
                request.session.pop("otp_user_id", None)
                return redirect("home:home")
            else:
                messages.error(request, "Invalid or expired code")
    else:#its a get
        form = OTPForm()

    return render(request, "OTP/verify_otp.html", {"form": form})



# def verify_signup_otp(request):
#     user_id = request.session.get("otp_user_id")
#     if not user_id:
#         return redirect("accounts:signup")

#     user = get_object_or_404(User, id=user_id)

#     if request.method == "POST":
#         form = OTPForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data["code"]

#             otp = EmailOTP.objects.filter(
#                 user=user,
#                 code=code
#             ).order_by("-created_at").first()

#             if otp and otp.is_valid():
#                 user.is_active = True
#                 user.save()

#                 otp.delete()
#                 request.session.pop("otp_user_id", None)

#                 login(request, user)
#                 return redirect("home:home")
#             else:
#                 messages.error(request, "Invalid or expired OTP")
#     else:
#         form = OTPForm()

#     return render(request, "OTP/verify_otp.html", {"form": form})

