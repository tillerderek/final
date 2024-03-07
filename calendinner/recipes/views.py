from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, RecipeStepForm, IngredientQuantityForm, IngredientForm, ingredient_formset, recipe_step_formset
from .models import Recipe, RecipeStep, IngredientQuantity, Ingredient
from django.forms import inlineformset_factory

@login_required
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    steps = RecipeStep.objects.filter(recipe=recipe)
    ingredients = IngredientQuantity.objects.filter(recipe=recipe)
    context = {
      'recipe': recipe,
      'ingredients': ingredients,
      'steps': steps}
    return render(request, 'recipes/recipe-detail.html', context)
  

@login_required
def submit_recipe(request):
    ingredient_formset = inlineformset_factory(Recipe, IngredientQuantity, fields=['ingredient', 'quantity', 'unit_measure'], extra=1)
    recipe_step_formset = inlineformset_factory(Recipe, RecipeStep, fields=['recipe_step'], extra=1, can_delete=False)

    if request.method == "POST":    
        recipe_form = RecipeForm(request.POST)
        ingredient_formset = ingredient_formset(request.POST, instance=recipe)
        step_formset = recipe_step_formset(request.POST, instance=recipe)

        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            recipe.save()

            ingredient_formset.instance = recipe
            ingredient_formset.save()

            step_formset.instance = recipe
            step_formset.save()

            return redirect('recipes/recipe-detail.html', recipe_id=recipe.id)
    else: 
        # Handle the case when the form is not valid
        return render(request, 'recipes/create-recipe.html')


def create_recipe(request):
    context = {
      'recipe_form': RecipeForm(),
    }
    return render(request, 'recipes/create-recipe.html', context)

def add_ingredient(request):
    recipe = Recipe()
    formset = ingredient_formset(instance=recipe)
    return render(request, 'recipes/add-ingredient.html', {'formset': formset})

def add_step(request):
    recipe = Recipe()
    formset = recipe_step_formset(instance=recipe)
    return render(request, 'recipes/add-step.html', {'formset': formset})
