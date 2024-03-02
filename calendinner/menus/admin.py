from django.contrib import admin

# Register your models here.
from .models import Menu, MenuRecipe, MenuRecipeQueue

admin.site.register(Menu)
admin.site.register(MenuRecipe)
admin.site.register(MenuRecipeQueue)
