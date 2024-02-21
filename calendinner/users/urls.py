from django.urls import path
from . import views

urlpatterns = [
    path("login", views.user_login, name="login"),
    path("signup", views.user_signup, name="signup"),
    path("logout", views.user_logout, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("favorites", views.favorites, name="favorites"),
    path("preferences", views.preferences, name="preferences"),
    path("uploaded", views.uploaded, name="uploaded"),
]
