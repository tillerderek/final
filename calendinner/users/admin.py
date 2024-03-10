from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UserRole)
admin.site.register(models.UserTagPreference)
admin.site.register(models.UserFavorite)