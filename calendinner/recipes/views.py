from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, RecipeStep, IngredientQuantity, Ingredient, Tag, UnitMeasure
from users.models import UserFavorite
from menus.models import Menu, MenuRecipe
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseNotFound

def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    steps = RecipeStep.objects.filter(recipe_id=recipe)
    ingredients = IngredientQuantity.objects.filter(recipe=recipe)
    favorite = UserFavorite.objects.filter(user=request.user, recipe=recipe).exists()
    in_menu = MenuRecipe.objects.filter(recipe=recipe, menu__user=request.user).exists()
    image = recipe.image
    
    context = {
      'recipe': recipe,
      'ingredients': ingredients,
      'steps': steps.all(),
      'user': request.user,
      'favorite': favorite,
      'in_menu': in_menu,
      'image': image,
    }
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
        image = request.FILES.get('image')
        tags = request.POST.getlist('tags')

        ingredients = request.POST.getlist('ingredient[]')
        quantities = request.POST.getlist('quantity[]')
        unit_measures = request.POST.getlist('unit_measure[]')
        steps = request.POST.getlist('step[]')

        recipe = Recipe(title=title, description=description, prep_time=prep_time, cook_time=cook_time, serving_size=serving_size, user=user, image=image)
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
    return render(request, 'recipes/create-recipe.html', context)

def add_ingredient(request):
    unit_measure = UnitMeasure.objects.all()
    return render(request, 'recipes/add-ingredient.html', {'unit_measure': unit_measure})

def add_step(request):
    return render(request, 'recipes/add-step.html')
  
# def scale_recipe(request, recipe_id):
#     # Get the recipe from the recipe_detail context (assuming it's passed)
#     recipe = request.GET.get('recipe')  # Access the recipe ID from query string

#     if not recipe:
#         return HttpResponseNotFound("Recipe not found")

#     # Access ingredients from the context (assuming it's passed)
#     ingredients = request.GET.get('ingredients')  # Access ingredients as a serialized string (optional)

#     if not ingredients:
#         return HttpResponseBadRequest("Missing ingredients data")

#     # Implement the scaling logic using the passed ingredients data
#     # (replace with your actual calculations based on the serialized ingredients data)
#     scaled_ingredients = []
#     # ... your scaling logic here ...

#     context = {'scaled_ingredients': scaled_ingredients}
#     return render(request, 'recipes/scale-recipe.html', context)

