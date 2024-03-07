from django.urls import path
from . import views

urlpatterns = [
    path('submit-recipe/', views.submit_recipe, name='submit_recipe'),
    path('recipe-detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('create-recipe/', views.create_recipe, name='create-recipe'),
    path('add-ingredient/', views.add_ingredient, name='add-ingredient'),
    path('add-step/', views.add_step, name='add-step'),
]
