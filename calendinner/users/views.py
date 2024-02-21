from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from . import forms
from .forms import LoginForm

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})
  
  # login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})
  
# logout page
def user_logout(request):
    logout(request)
    return redirect('home')
  
  
def dashboard(request):
    return render(request, 'users/dashboard.html')
  
def favorites(request):
    return render(request, 'users/favorites.html')
  
def preferences(request):
    return render(request, 'users/preferences.html')
  
def uploaded(request):
    return render(request, 'users/uploaded.html')