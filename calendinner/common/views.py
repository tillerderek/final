from django.shortcuts import render
import datetime
from .models import Recipe
from menus.models import Menu
from recipes.models import Ingredient




def home(request):
    recipes = Recipe.objects.all()
    
    context = {
        'recipes': recipes,
        'title': 'Dinner\'s Ready',
    }
    return render(request, 'common/home.html', context)
  
  
def autocomplete(request):
    term = request.POST.get('term', '')
    results = Ingredient.objects.filter(ingredient_name__icontains=term)
    return render(request, 'common/autocomplete_results.html', {'results': results})
