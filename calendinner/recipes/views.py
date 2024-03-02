from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, RecipeStepForm, IngredientQuantityForm, RecipeStepFormSet
from .models import Recipe, RecipeStep, IngredientQuantity, Ingredient
from django.forms import modelformset_factory


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipes/recipe-detail.html', {'recipe': recipe})

@login_required
def submit_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        ingredient_form = IngredientQuantityForm(request.POST)
        step_formset = RecipeStepFormSet(request.POST)
        

        if all([recipe_form.is_valid(), step_formset.is_valid(), ingredient_form.is_valid()]):
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            
            tags = request.POST.getlist('tags')
            recipe.tags.set(tags)
            
            for form in step_formset:
                step = form.save(commit=False)
                step.recipe = recipe
                step.save()

            ingredient = ingredient_form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
            
                        # Save tags associated with the recipe
            tags = request.POST.getlist('tags')
            recipe.tags.set(tags)

            return (redirect('recipe_detail', recipe_id=recipe.id))

    else:
        recipe_form = RecipeForm()
        step_formset = RecipeStepFormSet(queryset=RecipeStep.objects.none())
        ingredient_form = IngredientQuantityForm()

    context = {
        'recipe_form': recipe_form,
        'step_formset': step_formset,
        'ingredient_form': ingredient_form,
    }
    return render(request, 'recipes/submit-recipe.html', context)
  
def empty_step_form(request):
    form = RecipeStepForm()
    return render(request, 'recipes/empty_step_form.html', {'form': form})