from django.urls import path
from . import views

urlpatterns = [
    path("current-menu", views.current_menu, name="current-menu"),
    path("previous-menu", views.previous_menu, name="previous-menu"),
    path("upcoming-menu/", views.upcoming_menu, name="upcoming-menu"),
]

htmx_urlpatterns = [
    path("delete-upcoming-recipe/<int:recipe_id>", views.delete_upcoming_recipe, name="delete-upcoming-recipe"),
]

urlpatterns += htmx_urlpatterns