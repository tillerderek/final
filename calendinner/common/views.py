from django.shortcuts import render
import datetime
from .models import Recipe  # Assuming your models module is in the same directory as your views
from menus.models import Menu

def home(request):
    user = request.user
    current_week_number = datetime.date.today().isocalendar()[1]

    current_menu = Menu.objects.filter(user=user, date_start__week=current_week_number).first()
    if not current_menu:
        current_menu = Menu.objects.create(user=user, date_start=datetime.date.today())

    recipes = Recipe.objects.all()
    
    context = {
        'recipes': recipes,
        'title': 'Dinner\'s Ready',
    }
    return render(request, 'common/home.html', context)
