from django.db import models
from recipes.models import Tag, Recipe
from django.contrib.auth.models import User


# Create your models here.
class UserRole(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role


class User(models.Model):
    email = models.CharField(max_length=255)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role_id_usr = models.ForeignKey(UserRole, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fname} {self.lname}"


class UserTagPreference(models.Model):
    tag_id_utp = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user_id_utp = models.ForeignKey(User, on_delete=models.CASCADE)


class UserFavorite(models.Model):
    user_id_usf = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id_usf = models.ForeignKey(Recipe, on_delete=models.CASCADE)


def __str__(self):
    return self.title
