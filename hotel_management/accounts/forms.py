from django import forms

class SignInForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="First Name")
    last_name = forms.CharField(max_length=50, label="Last Name")
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")


class LogInForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
