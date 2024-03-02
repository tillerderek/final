from django.db import models
from recipes.models import Tag, Recipe
from django.contrib.auth.models import User


# Create your models here.
class UserRole(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role


class UserTagPreference(models.Model):
    tag= models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
