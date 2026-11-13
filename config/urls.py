from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from planner import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("recipes/", views.recipe_list, name="recipe_list"),
    path("recipes/add/", views.add_recipe, name="add_recipe"),
    path("recipes/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("planner/", views.weekly_planner, name="weekly_planner"),
    path("planner/delete/<int:pk>/", views.delete_meal, name="delete_meal"),
    path("groceries/", views.grocery_list, name="grocery_list"),
]
