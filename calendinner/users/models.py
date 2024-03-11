from django.db import models
from recipes.models import Tag, Recipe
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class UserTagPreference(models.Model):
    tag= models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_moderator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username