from django.shortcuts import render

from django.shortcuts import render, HttpResponse
from . import models

def home(request):
  recipes = models.Recipe.objects.all()
  context = {
    'recipes': recipes,
    'title': 'Dinner\'s Ready',
  }
  return render(request, 'common/home.html', context)
