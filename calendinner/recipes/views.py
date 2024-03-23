from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe, RecipeStep, IngredientQuantity, Ingredient, Tag, UnitMeasure
from users.models import UserFavorite
from menus.models import Menu, MenuRecipe

def recipe_detail(request, recipe_id):
    user = request.user
    recipe = Recipe.objects.get(id=recipe_id)
    steps = RecipeStep.objects.filter(recipe_id=recipe)
    ingredients = IngredientQuantity.objects.filter(recipe=recipe)
    image = recipe.image
    
    if request.user.is_authenticated:
        favorite = UserFavorite.objects.filter(user=user, recipe=recipe).exists()
        upcoming_menu = Menu.objects.filter(user=user, is_approved=False).first()
        in_menu = MenuRecipe.objects.filter(recipe=recipe, menu=upcoming_menu).exists()
        menu_recipe_count = MenuRecipe.objects.filter(menu=upcoming_menu).count()
    
        context = {
          'recipe': recipe,
          'ingredients': ingredients,
          'steps': steps.all(),
          'user': request.user,
          'favorite': favorite,
          'in_menu': in_menu,
          'image': image,
          'menu_recipe_count': menu_recipe_count,
        }
        return render(request, 'recipes/recipe-detail.html', context)
      
    else:
        context = {
          'recipe': recipe,
          'ingredients': ingredients,
          'steps': steps.all(),
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

@login_required
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

@login_required
def add_ingredient(request):
    unit_measure = UnitMeasure.objects.all()
    return render(request, 'recipes/add-ingredient.html', {'unit_measure': unit_measure})

@login_required
def add_step(request):
    return render(request, 'recipes/add-step.html')
