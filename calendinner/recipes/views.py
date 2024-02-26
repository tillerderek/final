from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, RecipeStepForm, IngredientQuantityForm
from .models import Recipe, RecipeStep, IngredientQuantity, Ingredient

def recipe_success(request):
    return render(request, 'recipes/recipe-success.html')

@login_required
def submit_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        step_form = RecipeStepForm(request.POST)
        ingredient_form = IngredientQuantityForm(request.POST)
        

        if all([recipe_form.is_valid(), step_form.is_valid(), ingredient_form.is_valid()]):
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            step_form.save()
            
                # Get the ingredient instance from the form data
            ingredient_instance = ingredient_form.cleaned_data['ingredient']
            ingredient = ingredient_form.save(commit=False)
            ingredient = ingredient_instance
            ingredient.save()

            return (redirect('recipe_success'))

    else:
        recipe_form = RecipeForm()
        step_form = RecipeStepForm()
        ingredient_form = IngredientQuantityForm()

    context = {
        'recipe_form': recipe_form,
        'step_form': step_form,
        'ingredient_form': ingredient_form,
    }
    return render(request, 'recipes/submit-recipe.html', context)