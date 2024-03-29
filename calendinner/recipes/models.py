from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    serving_size = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    image = models.ImageField(upload_to="static/images/recipe_images", blank=True)
    tags = models.ManyToManyField("Tag", through="RecipeTag")
    ingredients = models.ManyToManyField("Ingredient", through="IngredientQuantity")
    steps = models.ManyToManyField("RecipeStep")

    def __str__(self):
        return self.title

class RecipeStep(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=1)
    recipe_step = models.CharField(max_length=2000)
    
    def __str__(self):
        return self.recipe_step

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.ingredient_name


class UnitMeasure(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    unit_measure = models.ForeignKey(UnitMeasure, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} {self.unit_measure} of {self.ingredient}"


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
