from django.db import models

class UnitMeasure(models.Model):
    name = models.CharField(max_length=40)

class UserRole(models.Model):
    role = models.CharField(max_length=50)

class User(models.Model):
    email = models.CharField(max_length=255)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role_id_usr = models.ForeignKey(UserRole, on_delete=models.CASCADE)

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)
    tag_description = models.CharField(max_length=1000)

class UserTagPreference(models.Model):
    tag_id_utp = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user_id_utp = models.ForeignKey(User, on_delete=models.CASCADE)

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    prep_time = models.TimeField()
    cook_time = models.TimeField()
    serving_size = models.IntegerField()
    user_id_rec = models.ForeignKey(User, on_delete=models.CASCADE)
    image_filename = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, through='RecipeTag')

class Menu(models.Model):
    user_id_men = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_start = models.DateTimeField()
    is_approved = models.BooleanField()

class MenuRecipe(models.Model):
    recipe_id_mnr = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    menu_id_mnr = models.ForeignKey(Menu, on_delete=models.CASCADE)

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)

class RecipeIngredient(models.Model):
    ingredient_id_rpi = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    recipe_id_rpi = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    unit_measure_id_rpi = models.ForeignKey(UnitMeasure, on_delete=models.CASCADE)

class MenuRecipeQueue(models.Model):
    user_id_mrq = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id_mrq = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class UserFavorite(models.Model):
    user_id_usf = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id_usf = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class RecipeTag(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
