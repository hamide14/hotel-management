from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2')




class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11 , label="Phone Number")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class EmailForm(forms.Form):
    email = forms.EmailField(label="Email")


class OTPForm(forms.Form):
    code = forms.CharField(max_length=6, label="OTP Code")
