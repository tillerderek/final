from django.shortcuts import render
from .models import Recipe

def recipe_card(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'recipes/recipe_card.html', {'recipe': recipe})