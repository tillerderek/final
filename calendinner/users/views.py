from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from . import forms
from .forms import LoginForm, SignupForm
from .models import Recipe, UserFavorite
from menus.models import Menu, MenuRecipe
from django.utils import timezone

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.full_clean()
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
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
  
@login_required
def favorites(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')

        user = request.user  

        if not UserFavorite.objects.filter(user=user.id, recipe=recipe_id).exists():

            recipe = Recipe.objects.get(pk=recipe_id)
            favorite = UserFavorite(user=user, recipe=recipe)
            favorite.save()

        return redirect('favorites')

    favorites = UserFavorite.objects.filter(user=request.user.id)

    context = {
        'favorites': favorites,
        'title': 'Favorites',
    }

    return render(request, 'users/favorites.html', context)

  
def preferences(request):
    return render(request, 'users/preferences.html')
  
def uploaded(request):
    userUploaded = Recipe.objects.filter(user=request.user)
    
    return render(request, 'users/uploaded.html', {'userUploaded': userUploaded})