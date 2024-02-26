from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Recipe)
admin.site.register(models.Ingredient)
admin.site.register(models.IngredientQuantity)
admin.site.register(models.Tag)
admin.site.register(models.RecipeTag)
admin.site.register(models.UnitMeasure)
admin.site.register(models.RecipeStep)