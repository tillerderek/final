from django.urls import path
from . import views

urlpatterns = [
    path("<int:recipe_id>/", views.recipe_card, name="recipe_card"),
    path("recipe-detail/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path("add-recipe", views.add_recipe, name="add-recipe"),
]
