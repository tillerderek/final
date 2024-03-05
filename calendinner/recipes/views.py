from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, RecipeStepForm, IngredientQuantityForm, IngredientForm, recipe_step_formset, ingredient_quantity_formset, ingredient_formset
from .models import Recipe, RecipeStep, IngredientQuantity, Ingredient
from django.forms import modelformset_factory

@login_required
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredient = Ingredient.objects.get(id=recipe_id)
    step = RecipeStep.objects.get(id=recipe_id)
    context = {'recipe': recipe,
               'ingredient': ingredient,
               'step': step}
    return render(request, 'recipes/recipe-detail.html', context)

@login_required
def submit_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        step_formset = recipe_step_formset(request.POST)
        ingredient_form = ingredient_formset(request.POST)
        ingredient_quantity_form = ingredient_quantity_formset(request.POST)
        
        if recipe_form.is_valid() and step_formset.is_valid() and ingredient_form.is_valid() and ingredient_quantity_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            
            for form in step_formset:
                step = form.save(commit=False)
                step.recipe = recipe
                step.save()
                
            for form in ingredient_form:
                if form.is_valid():
                  ingredient_name = form.cleaned_data['ingredient_name']
                  if Ingredient.objects.filter(ingredient_name=ingredient_name).exists():
                    ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)
                  else:
                    # Ingredient doesn't exist, create a new one
                    ingredient = Ingredient.objects.create(ingredient_name=ingredient_name)

                
            for form in ingredient_quantity_form:
                ingredient_quantity = form.save(commit=False)
                ingredient_quantity.recipe = recipe
                ingredient_quantity.ingredient = ingredient
                ingredient_quantity.save()
                
            return render(request, 'recipes/submit-recipe.html', {'recipe_form': recipe_form, 'step_formset': step_formset, 'ingredient_form': ingredient_form, 'ingredient_quantity_form': ingredient_quantity_form, 'success': True})
        else:
            return HttpResponse('Form is not valid.')
    else:
        recipe_form = RecipeForm()
        step_formset = recipe_step_formset(queryset=RecipeStep.objects.none())
        ingredient_form = ingredient_formset(queryset=Ingredient.objects.none())
        ingredient_quantity_form = ingredient_quantity_formset(queryset=IngredientQuantity.objects.none())
        
        context = {'recipe_form': recipe_form,
                   'step_formset': step_formset,
                   'ingredient_form': ingredient_form,
                   'ingredient_quantity_form': ingredient_quantity_form}
        
        return render(request, 'recipes/submit-recipe.html', context)

@login_required
def empty_step_form(request):
    form = RecipeStepForm()
    context = {'form': form}
    return render(request, 'recipes/empty-step-form.html', context)

@login_required
def empty_ingredient_form(request):
    quantity_form = IngredientQuantityForm()
    ingredient_form = IngredientForm()
    context = {'form': ingredient_form, 'quantity_form': quantity_form}
    return render(request, 'recipes/empty-ingredient-form.html', context)
