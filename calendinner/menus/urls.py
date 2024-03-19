from django.urls import path
from . import views

urlpatterns = [
    path("current-menu", views.current_menu, name="current-menu"),
    path("previous-menu", views.previous_menu, name="previous-menu"),
    path("upcoming-menu/", views.upcoming_menu, name="upcoming-menu"),
    path("process-draft-menus", views.process_draft_menus, name="process-draft-menus"),
    path("process-final-menus", views.process_final_menus, name="process-final-menus"),
    path("delete-upcoming-recipe/<int:recipe_id>/", views.delete_upcoming_recipe, name="delete-upcoming-recipe"),
    path("approve-menu/", views.approve_menu, name="approve-menu"),
]