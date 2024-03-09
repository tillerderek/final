from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, RecipeStepForm, IngredientQuantityForm, IngredientForm, ingredient_formset, recipe_step_formset
from .models import Recipe, RecipeStep, IngredientQuantity, Ingredient, Tag, UnitMeasure
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404


@login_required
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    steps = RecipeStep.objects.filter(recipe_id=recipe)
    ingredients = IngredientQuantity.objects.filter(recipe=recipe)
    context = {
      'recipe': recipe,
      'ingredients': ingredients,
      'steps': steps.all()}
    return render(request, 'recipes/recipe-detail.html', context)
  

@login_required
def submit_recipe(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        prep_time = request.POST['prep_time']
        cook_time = request.POST['cook_time']
        serving_size = request.POST['servings']
        user = request.user
        image_filename = request.POST['image_filename']
        tags = request.POST.getlist('tags')

        ingredients = request.POST.getlist('ingredient[]')
        quantities = request.POST.getlist('quantity[]')
        unit_measures = request.POST.getlist('unit_measure[]')
        steps = request.POST.getlist('step[]')

        recipe = Recipe(title=title, description=description, prep_time=prep_time, cook_time=cook_time, serving_size=serving_size, user=user, image_filename=image_filename)
        recipe.save()
        recipe.tags.add(*tags)

        for ingredient, quantity, unit_measure_id in zip(ingredients, quantities, unit_measures):
            ingredient, _ = Ingredient.objects.get_or_create(ingredient_name=ingredient)
            unit_measure = get_object_or_404(UnitMeasure, id=unit_measure_id)
            ingredient_quantity = IngredientQuantity(ingredient=ingredient, quantity=quantity, recipe=recipe, unit_measure=unit_measure)
            ingredient_quantity.save()

        for step in steps:
            step_obj = RecipeStep(recipe_id=recipe, recipe_step=step)
            step_obj.save()

        return redirect('recipe_detail', recipe_id=recipe.id)


def create_recipe(request):
    tags = Tag.objects.all()
    unit_measure = UnitMeasure.objects.all()
    context = {
      'recipe': Recipe(),
      'recipe_step': RecipeStep(),
      'ingredient_quantity': IngredientQuantity(),
      'ingredient': Ingredient(),
      'tags': tags,
      'unit_measure': unit_measure,
    }
    # context = {
    #   'recipe_form': RecipeForm(),
    # }
    return render(request, 'recipes/create-recipe.html', context)

def add_ingredient(request):
    unit_measure = UnitMeasure.objects.all()
    return render(request, 'recipes/add-ingredient.html', {'unit_measure': unit_measure})
    # recipe = Recipe()
    # formset = ingredient_formset(instance=recipe)
    # return render(request, 'recipes/add-ingredient.html', {'formset': formset})

def add_step(request):
    recipe = Recipe()
    formset = recipe_step_formset(instance=recipe)
    return render(request, 'recipes/add-step.html', {'formset': formset})
