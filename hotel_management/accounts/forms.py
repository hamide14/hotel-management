from django import forms
from django.contrib.auth.forms import UserCreationForm # defult form for login
from .models import CustomUser # our custom user model

#modelform is directly linked to a model 
class CustomUserCreationForm(UserCreationForm):
    # meta shows used model and form fields
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2')
    # data will directly saved to customUser model




class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11 , label="Phone Number")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

#form for edit user info 
# modelForm means the changes will be directly saved to customuser
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']

#simple form for email input , usef for otp
class EmailForm(forms.Form):
    email = forms.EmailField(label="Email")

#form for otp input
class OTPForm(forms.Form):
    code = forms.CharField(max_length=6, label="OTP Code")
