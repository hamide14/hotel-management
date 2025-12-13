# views.py
from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin_done')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signin/signin.html', {'form': form})


def signin_done(request):
    return render(request, 'signin/signin_done.html')


def login_page(request):
    return render(request, 'login/login.html')
