from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Menu, MenuRecipe, User
from recipes.models import Recipe
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest

@login_required
def current_menu(request):
    current_menu = Menu.objects.filter(is_approved=True).first()
    current_recipes = MenuRecipe.objects.filter(menu=current_menu)
    
    return render(request, 'menus/current-menu.html', {'current_recipes': current_recipes})
  
@login_required
def previous_menu(request):
    previous_menus = Menu.objects.filter(is_approved=True, date_start__lt=timezone.now()).order_by('-date_start')[:2]
    
    for previous_menu in previous_menus:
        previous_menu.recipes = MenuRecipe.objects.filter(menu=previous_menu)
        
    context = {
        'previous_menus': previous_menus
    }
        
    return render(request, 'menus/previous-menu.html', context)
  
@login_required
def upcoming_menu(request):
    upcoming_recipe = None
    recipe_id = None
    
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        user = request.user
        recipe = Recipe.objects.get(pk=recipe_id)
        
        upcoming_menu = Menu.objects.filter(user=user, date_start__lt=timezone.now() + timezone.timedelta(days=7), is_approved=False).first()
        
        if not upcoming_menu:
            upcoming_menu = Menu.objects.create(user=user, date_created=timezone.now(), date_start=timezone.now(), is_approved=False)
        
        if not MenuRecipe.objects.filter(menu=upcoming_menu, recipe=recipe).exists():
            menu_recipe = MenuRecipe(menu=upcoming_menu, recipe=recipe)
            menu_recipe.save()
            
        return HttpResponse('Added to Menu', status=200)

    user = request.user
    upcoming_menu = Menu.objects.filter(user=user, date_created__lt=timezone.now() + timezone.timedelta(days=7), is_approved=False).first()
    
    if not upcoming_menu:
        upcoming_menu = Menu.objects.create(user=user, date_created=timezone.now(), date_start=timezone.now(), is_approved=False)
    
    upcoming_recipe = MenuRecipe.objects.filter(menu=upcoming_menu)
    
    return render(request, 'menus/upcoming-menu.html', {'upcoming_recipe': upcoming_recipe})

@login_required
@require_http_methods(["DELETE"])
def delete_upcoming_recipe(request, recipe_id):
    user = request.user
    upcoming_menu = Menu.objects.filter(user=user, is_approved=False).first()

    if not upcoming_menu:
        return HttpResponseBadRequest("No upcoming menu found")

    # Retrieve all MenuRecipe objects associated with the upcoming menu and the given recipe_id
    upcoming_recipes = MenuRecipe.objects.filter(menu=upcoming_menu, recipe__pk=recipe_id)

    # Check if any MenuRecipe objects are found
    if upcoming_recipes.exists():
        # Delete all found MenuRecipe objects
        upcoming_recipes.delete()
        # After deletion, retrieve the updated list of upcoming recipes
        upcoming_recipe = MenuRecipe.objects.filter(menu=upcoming_menu)
        return render(request, 'menus/upcoming-menu.html', {'upcoming_recipe': upcoming_recipe})
    else:
        return HttpResponseBadRequest("No matching recipe found in the upcoming menu")

def process_draft_menus(request):
    if request.headers.get('Api-Key') == 'zany1061':
      users = User.objects.all()
      json_responses = []
      
      for user in users:
        upcoming_menu = Menu.objects.filter(user=user, date_start__lt=timezone.now() + timezone.timedelta(days=7), is_approved=False).first()
        
        if not upcoming_menu:
            upcoming_menu = Menu.objects.create(user=user, date_created=timezone.now(), date_start=timezone.now() + timezone.timedelta(days=3), is_approved=False)
        
        upcoming_recipes = MenuRecipe.objects.filter(menu=upcoming_menu)
            
        if upcoming_recipes.count() < 7:
            used_recipes = list(upcoming_recipes.values_list('recipe_id', flat=True))

            for i in range(7 - upcoming_recipes.count()):
                recipe = Recipe.objects.exclude(pk__in=used_recipes).order_by('?').first()
                used_recipes.append(recipe.id)
                menu_recipe = MenuRecipe(menu=upcoming_menu, recipe=recipe)
                menu_recipe.save()
      
        current_menu_recipes = MenuRecipe.objects.filter(menu=upcoming_menu)
        current_recipes_titles = list([recipe.recipe.title for recipe in current_menu_recipes])
        
        json_data = {
            'recipes': current_recipes_titles,
            'link': 'https://calendinner.com/menus/upcoming-menu',
            'email': user.email,
            'name': user.first_name
        }
        json_responses.append(json_data)
        
      return JsonResponse(json_responses, safe=False, status=200)
    else:
        return HttpResponse('Unauthorized', status=401)

  
def process_final_menus(request):
    users = user.objects.all()
    
    for user in users:
        upcoming_menu = Menu.objects.filter(is_approved=False).first()    
        upcoming_menu.is_approved = True
                
    return HttpResponse('Success', status=200)
  
  
def approve_menu(request):
    if request.method == 'PATCH':
      user = request.user
      upcoming_menu = Menu.objects.filter(user=user, is_approved=False).first()
      upcoming_menu.is_approved = True
      upcoming_menu.save()
    
      return HttpResponse('Menu Approved!', status=200)