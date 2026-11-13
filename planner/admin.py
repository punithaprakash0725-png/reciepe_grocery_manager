from django.contrib import admin
from .models import Recipe, MealPlan

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "cooking_time", "is_approved", "created_by")
    list_filter = ("category", "is_approved")
    search_fields = ("title", "ingredients")
    list_editable = ("is_approved",)

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ("user", "day", "meal_type", "recipe", "week_start")
    list_filter = ("week_start", "day", "meal_type")
