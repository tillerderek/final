from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, RecipeStepForm, IngredientQuantityForm, IngredientForm, ingredient_formset, recipe_step_formset
from .models import Recipe, RecipeStep, IngredientQuantity, Ingredient, Tag, UnitMeasure
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

    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        prep_time = request.POST['prep_time']
        cook_time = request.POST['cook_time']
        serving_size = request.POST['servings']
        user = request.user
        image_filename = request.POST['image_filename']
        tags = request.POST['tags']
        ingredient = request.POST['ingredient']
        quantity = request.POST['quantity']
        unit_measure = request.POST['unit_measure']
        step = request.POST['step']
        recipe = Recipe(title=title, description=description, prep_time=prep_time, cook_time=cook_time, serving_size=serving_size, user=user, image_filename=image_filename)
        recipe.save()
        recipe.tags.add(tags)
        #check if ingredient exists in the database and if not, add it to the database and then add it to the recipe 
        ingredient = Ingredient.objects.get_or_create(ingredient_name=ingredient)
        ingredient = ingredient[0]
        ingredient.save()
        unit_measure = UnitMeasure.objects.get(pk=unit_measure)
        ingredient_quantity = IngredientQuantity(ingredient=ingredient, quantity=quantity, recipe=recipe, unit_measure=unit_measure)
        ingredient_quantity.save()
        recipe_step = RecipeStep(recipe_id=recipe, recipe_step=step)
        recipe_step.save()
        
        return redirect('recipe_detail', recipe_id=recipe.id)
        
        
    # ingredient_formset = inlineformset_factory(Recipe, IngredientQuantity, fields=['ingredient', 'quantity', 'unit_measure'], extra=1)
    # recipe_step_formset = inlineformset_factory(Recipe, RecipeStep, fields=['recipe_step'], extra=1, can_delete=False)

    # if request.method == "POST":    
    #     recipe_form = RecipeForm(request.POST)
    #     ingredient_formset = ingredient_formset(request.POST, instance=recipe)
    #     step_formset = recipe_step_formset(request.POST, instance=recipe)

    #     if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
    #         recipe = recipe_form.save(commit=False)
    #         recipe.user = request.user
    #         recipe.save()

    #         ingredient_formset.instance = recipe
    #         ingredient_formset.save()

    #         step_formset.instance = recipe
    #         step_formset.save()

    #         return redirect('recipes/recipe-detail.html', recipe_id=recipe.id)
    # else: 
    #     # Handle the case when the form is not valid
    #     return render(request, 'recipes/create-recipe.html')


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
