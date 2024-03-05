from django.shortcuts import render
import datetime
from .models import Recipe
from menus.models import Menu




def home(request):
    user = request.user if request.user.is_authenticated else None
    current_week_number = datetime.date.today().isocalendar()[1]

    recipes = Recipe.objects.all()
    
    context = {
        'recipes': recipes,
        'title': 'Dinner\'s Ready',
    }
    return render(request, 'common/home.html', context)
  
  
def autocomplete(request):
    term = request.GET.get('term', '')
    results = Recipe.objects.filter(title__icontains=term)
    return render(request, 'common/autocomplete_results.html', {'results': results})
