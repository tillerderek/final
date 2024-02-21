from django.db import models
from recipes.models import Recipe
from django.contrib.auth.models import User


# Create your models here.
class Menu(models.Model):
    user_id_men = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_start = models.DateTimeField()
    is_approved = models.BooleanField()

    def __str__(self):
        return self.is_approved


class MenuRecipe(models.Model):
    recipe_id_mnr = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    menu_id_mnr = models.ForeignKey(Menu, on_delete=models.CASCADE)


class MenuRecipeQueue(models.Model):
    user_id_mrq = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id_mrq = models.ForeignKey(Recipe, on_delete=models.CASCADE)
