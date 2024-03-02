from django.shortcuts import render
import datetime
from .models import Recipe  # Assuming your models module is in the same directory as your views
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
