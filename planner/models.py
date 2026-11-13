from django.conf import settings
from django.db import models

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ("Breakfast", "Breakfast"), ("Lunch", "Lunch"),
        ("Dinner", "Dinner"), ("Snack", "Snack"),
    ]
    title = models.CharField(max_length=160)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    ingredients = models.TextField(help_text="Enter one ingredient per line. Example: Rice - 1 cup")
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField(default=20, help_text="Minutes")
    image = models.FileField(upload_to="recipes/", blank=True, help_text="Optional photo of the dish")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def emoji(self):
        t = self.title.lower()
        for words, icon in [
            (("dosa", "chilla"), "🥞"), (("paratha", "chapati", "bhature"), "🫓"),
            (("soup",), "🥣"), (("biryani", "pulao", "rice", "khichdi"), "🍚"),
            (("chole",), "🫘"), (("paneer",), "🧀"), (("dal",), "🍲"),
            (("poha", "upma", "idli"), "🍛"), (("curry", "masala"), "🍛"),
        ]:
            if any(w in t for w in words):
                return icon
        return {"Breakfast": "🍳", "Lunch": "🍛", "Dinner": "🍲"}.get(self.category, "🍽️")
        
    def ingredient_lines(self):
        return [line.strip() for line in self.ingredients.splitlines() if line.strip()]

class MealPlan(models.Model):
    DAYS = [(d, d) for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
    MEALS = [("Breakfast", "Breakfast"), ("Lunch", "Lunch"), ("Dinner", "Dinner")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    day = models.CharField(max_length=12, choices=DAYS)
    meal_type = models.CharField(max_length=12, choices=MEALS)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    week_start = models.DateField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "day", "meal_type", "week_start"], name="unique_user_meal_slot")]
        ordering = ["week_start", "day", "meal_type"]

    def __str__(self):
        return f"{self.user} - {self.day} - {self.meal_type}"