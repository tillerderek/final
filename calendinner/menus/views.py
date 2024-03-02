from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Menu, MenuRecipe
from recipes.models import Recipe
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.
def current_menu(request):
    return render(request, 'menus/current-menu.html')
  
def previous_menu(request):
    return render(request, 'menus/previous-menu.html')
  
@login_required
def upcoming_menu(request):
    upcoming_recipe = None
    recipe_id = None
    
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        user = request.user
        recipe = Recipe.objects.get(pk=recipe_id)
        
        upcoming_menu = Menu.objects.filter(user=user, date_created__lt=timezone.now() + timezone.timedelta(days=7), is_approved=False).first()
        
        if not upcoming_menu:
            upcoming_menu = Menu.objects.create(user=user, date_created=timezone.now(), date_start=timezone.now()) ##maybe switch to timedelta(days=7)
        
        if not MenuRecipe.objects.filter(menu=upcoming_menu, recipe=recipe).exists():
            menu_recipe = MenuRecipe(menu=upcoming_menu, recipe=recipe)
            menu_recipe.save()

    user = request.user
    upcoming_menu = Menu.objects.filter(user=user, date_created__lt=timezone.now() + timezone.timedelta(days=7), is_approved=False).first()
    
    if not upcoming_menu:
        upcoming_menu = Menu.objects.create(user=user, date_created=timezone.now(), date_start=timezone.now())
    
    upcoming_recipe = MenuRecipe.objects.filter(menu=upcoming_menu)
    
    return render(request, 'menus/upcoming-menu.html', {'upcoming_recipe': upcoming_recipe})
  

def delete_upcoming_recipe(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(MenuRecipe, recipe__pk=recipe_id, menu__user=user)
    recipe.delete()
    
    upcoming_recipe = MenuRecipe.objects.all()
    return render(request, 'menus/upcoming-menu.html', {'upcoming_recipe': upcoming_recipe})
