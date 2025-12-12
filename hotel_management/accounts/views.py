from django.shortcuts import render
from .forms import SignInForm, LogInForm

def SignIn(request):
    form = SignInForm()
    return render(request, 'signin/signin.html', {'form': form})


def LogIn(request):
    form = LogInForm()
    return render(request, 'login/login.html', {'form': form})
