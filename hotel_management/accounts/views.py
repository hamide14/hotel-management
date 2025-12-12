from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignInForm, LogInForm


def SignIn(request):
    form = SignInForm()
    return render(request, 'signin/signin.html', {'form': form})



def LogIn(request):
    pass
