from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from . import forms
from .forms import LoginForm, SignupForm
from .models import Recipe, UserFavorite, UserProfile
from menus.models import Menu, MenuRecipe
from django.utils import timezone
from django.http import HttpResponse

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
  
  
  
@login_required
def favorites(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        user = request.user  

        if not UserFavorite.objects.filter(user=user.id, recipe=recipe_id).exists():
            recipe = Recipe.objects.get(pk=recipe_id)
            favorite = UserFavorite(user=user, recipe=recipe)
            favorite.save()

        return HttpResponse("Added to favorites")

    favorites = UserFavorite.objects.filter(user=request.user.id)

    context = {
        'favorites': favorites,
        'title': 'Favorites',
    }

    return render(request, 'users/favorites.html', context)

@require_http_methods(["DELETE"])
def delete_favorite(request, recipe_id):
    user = request.user
    recipe = Recipe.objects.get(pk=recipe_id)
    favorite = UserFavorite.objects.filter(user=user, recipe=recipe)
    favorite.delete()
    
    favorites = UserFavorite.objects.filter(user=request.user.id)
    return render(request, 'users/favorites.html', {'favorites': favorites})

  
def preferences(request):
    return render(request, 'users/preferences.html')
  
def uploaded(request):
    userUploaded = Recipe.objects.filter(user=request.user)
    
    return render(request, 'users/uploaded.html', {'userUploaded': userUploaded})
  
def moderator_content(request):
    return render(request, 'users/moderator-content.html')
  
  
def dashboard(request):
    user_profile = request.user.userprofile
    is_moderator = user_profile.is_moderator
    return render(request, 'users/dashboard.html', {'is_moderator': is_moderator})