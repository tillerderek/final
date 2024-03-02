from django.db import models
from recipes.models import Recipe
from django.contrib.auth.models import User


# Create your models here.
class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_start = models.DateTimeField()
    is_approved = models.BooleanField()
    

class MenuRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)


class MenuRecipeQueue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)