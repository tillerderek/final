from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Menu, MenuRecipe, User
from recipes.models import Recipe
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
def current_menu(request):
    ## where user=user filter Menu by approved=True and is .first() also return nothing here yet if nothing here
    return render(request, 'menus/current-menu.html')
  
def previous_menu(request):
    ## where user=user filter Menu by approved=True and is not .first() also return nothing here yet if nothing here
    return render(request, 'menus/previous-menu.html')
  
@login_required
def upcoming_menu(request):
    upcoming_recipe = None
    recipe_id = None
    
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        user = request.user
        recipe = Recipe.objects.get(pk=recipe_id)
        
        upcoming_menu = Menu.objects.filter(user=user, date_start__lt=timezone.now() + timezone.timedelta(days=7), is_approved=False).first()

        # schedule is fixed and the same for everyone
            # date_draft is always the next FRIDAY (user gets notification of draft menu)
            # date_start is always the next MONDAY (finalized menu gets locked in)

        # scenario
            # log in on Saturday as fresh user
            # has upcoming menu? NO
                # NEW upcoming_menu
                    # date_draft is ~6 days from now (Friday)
                    # date_start is ~9 days from now (Monday)

        
        if not upcoming_menu:
            upcoming_menu = Menu.objects.create(user=user, date_created=timezone.now(), date_start=timezone.now(), is_approved=False) ##maybe switch to timedelta(days=7)
        
        if not MenuRecipe.objects.filter(menu=upcoming_menu, recipe=recipe).exists():
            menu_recipe = MenuRecipe(menu=upcoming_menu, recipe=recipe)
            menu_recipe.save()

    user = request.user
    upcoming_menu = Menu.objects.filter(user=user, date_created__lt=timezone.now() + timezone.timedelta(days=7), is_approved=False).first()
    
    if not upcoming_menu:
        upcoming_menu = Menu.objects.create(user=user, date_created=timezone.now(), date_start=timezone.now())
    
    upcoming_recipe = MenuRecipe.objects.filter(menu=upcoming_menu)
    
    return render(request, 'menus/upcoming-menu.html', {'upcoming_recipe': upcoming_recipe})
  
  
  # check how many recipes in menu.first(), fill to 7. then fill menu recipe queue with 21 recipes. this all happens 3 days prior to upcoming menu start date. 

def delete_upcoming_recipe(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(MenuRecipe, recipe__pk=recipe_id, menu__user=user)
    recipe.delete()
    
    upcoming_recipe = MenuRecipe.objects.all(pk=user)
    return HttpResponse('it works')
    return render(request, 'menus/upcoming-menu.html', {'upcoming_recipe': upcoming_recipe})
  
def process_draft_menus(request):
    if request.headers.get('Api-Key') == 'zany1061':
      users = User.objects.all()
      for user in users:
        
        upcoming_menu = Menu.objects.filter(user=user, date_start__lt=timezone.now() + timezone.timedelta(days=7), is_approved=False).first()
        
        if not upcoming_menu:
            upcoming_menu = Menu.objects.create(user=user, date_created=timezone.now(), date_start=timezone.now() + timezone.timedelta(days=3), is_approved=False)
        
        upcoming_recipes = MenuRecipe.objects.filter(menu=upcoming_menu)
            
        if upcoming_recipes.count() < 7:
            used_recipes = list(upcoming_recipes.values_list('recipe_id', flat=True))
            # t = json.dumps(used_recipes)
            # return used_recipes

            for i in range(7 - upcoming_recipes.count()):
                recipe = Recipe.objects.exclude(pk__in=used_recipes).order_by('?').first()
                used_recipes.append(recipe.id)
                menu_recipe = MenuRecipe(menu=upcoming_menu, recipe=recipe)
                menu_recipe.save()
        
        # create json object with:
            # list of recipe names
            # link to menu page
            # user's email address
            # users name
        
        # send json requestlist to Amazon SES API endpoint to send email
        current_menu_recipes = MenuRecipe.objects.filter(menu=upcoming_menu)
        # current_recipes = current_menu_recipes.prefetch_related('recipes')
        current_recipes_titles = list([recipe.recipe.title for recipe in current_menu_recipes])
        
        json = {
            # 'recipes': serializers.serialize('json', upcoming_recipes),
            # 'recipes': current_recipes_titles.values_list('title'),
            # 'recipes': serializers.serialize('json', current_recipes_titles),
            'recipes': current_recipes_titles,
            'link': 'https://calendinner.com/menus/upcoming-menu',
            'email': user.email,
            'name': user.first_name
        }
        return JsonResponse(json)
    else:
        return HttpResponse('Unauthorized', status=401)

  
def process_final_menus(request):
    users = user.objects.all()
    
    for user in users:
        upcoming_menu = Menu.objects.filter(is_approved=False).first()    
        upcoming_menu.is_approved = True
                
    return HttpResponse('Success', status=200)