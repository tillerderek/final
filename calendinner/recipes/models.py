from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    serving_size = models.IntegerField()
    user_id_rec = models.ForeignKey(User, on_delete=models.CASCADE)
    image_filename = models.CharField(max_length=255)
    tags = models.ManyToManyField("Tag", through="RecipeTag")

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)

    def __str__(self):
        return self.ingredient_name


class UnitMeasure(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient_id_rpi = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    recipe_id_rpi = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    unit_measure_id_rpi = models.ForeignKey(UnitMeasure, on_delete=models.CASCADE)

    def __str__(self):
        return self.quantity


class Tag(models.Model):
    tag_name = models.CharField(max_length=255)
    tag_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.tag_name


class RecipeTag(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe_id.title
