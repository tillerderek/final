from django.urls import path
from . import views

urlpatterns = [
    # path("<int:recipe_id>/", views.recipe_card, name="recipe_card"),
    # path("recipe-detail/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path('submit-recipe/', views.submit_recipe, name='submit_recipe'),
    path('recipe-detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('empty-step-form/', views.empty_step_form, name='empty-step-form')
]
