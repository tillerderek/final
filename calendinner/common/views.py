from django.shortcuts import render
import datetime
from .models import Recipe
from menus.models import Menu
from recipes.models import Ingredient




def home(request):
    recipes = Recipe.objects.all()
    if request.user.is_authenticated:
      user_profile = request.user.userprofile
      is_moderator = user_profile.is_moderator
      
      context = {
        'recipes': recipes,
        'title': 'Dinner\'s Ready',
        'is_moderator': is_moderator,
    }
    else:
      context = {
        'recipes': recipes,
        'title': 'Dinner\'s Ready',
    }
    return render(request, 'common/home.html', context)
  
def search(request):
    query = request.GET.get('term', '')
    recipes = Recipe.objects.filter(title__icontains=query)
    # ingredients = Recipe.objects.filter(ingredients__icontains=query)
    context = {
        'recipes': recipes,
        # 'ingredients': ingredients,
        'title': 'Search results',
        'query': query,
    }
    return render(request, 'common/search.html', context)
  
  
def autocomplete(request):
    term = request.POST.get('term', '')
    results = Ingredient.objects.filter(ingredient_name__icontains=term)
    return render(request, 'common/autocomplete_results.html', {'results': results})
