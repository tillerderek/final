from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    recipe_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    serving_size = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_filename = models.CharField(max_length=255)
    
class Ingredient(models.Model):
    ingredient_id = models.IntegerField(primary_key=True)
    ingredient_name = models.CharField(max_length=255)

class UnitMeasure(models.Model):
    unit_measure_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)    

class RecipeIngredient(models.Model):
    recipe_ingredient_id = models.IntegerField(primary_key=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    unit_measure = models.ForeignKey(UnitMeasure, on_delete=models.CASCADE)
    
def __str__(self):
    return self.title