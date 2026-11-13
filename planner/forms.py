from django import forms
from django.contrib.auth.models import User
from .models import Recipe, MealPlan

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    class Meta:
        model = User
        fields = ["username", "email", "password"]
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "category", "description", "ingredients", "instructions", "cooking_time"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "ingredients": forms.Textarea(attrs={"rows": 6}),
            "instructions": forms.Textarea(attrs={"rows": 6}),
        }

class MealPlanForm(forms.ModelForm):
    """Week is set automatically in the view (current week, Monday start)."""
    class Meta:
        model = MealPlan
        fields = ["day", "meal_type", "recipe"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["recipe"].queryset = Recipe.objects.filter(is_approved=True).order_by("title")
        self.fields["recipe"].empty_label = "Choose a recipe"
