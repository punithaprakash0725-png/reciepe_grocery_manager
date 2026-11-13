import re
from datetime import date, timedelta
from collections import OrderedDict
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import RegisterForm, RecipeForm, MealPlanForm
from .models import Recipe, MealPlan

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MEALS = ["Breakfast", "Lunch", "Dinner"]


def site_stats():
    return {
        "member_count": get_user_model().objects.count(),
        "recipe_count": Recipe.objects.filter(is_approved=True).count(),
        "total_plan_count": MealPlan.objects.count(),
    }


def home(request):
    recipes = Recipe.objects.filter(is_approved=True).order_by("-created_at")[:6]
    return render(request, "home.html", {"recipes": recipes, **site_stats()})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    is_admin = request.user.is_staff or request.user.is_superuser
    context = {
        **site_stats(),
        "plan_count": MealPlan.objects.filter(user=request.user).count(),
        "is_admin": is_admin,
    }
    if is_admin:
        context["recent_members"] = get_user_model().objects.order_by("-date_joined")[:5]
        context["pending_count"] = Recipe.objects.filter(is_approved=False).count()
    return render(request, "dashboard.html", context)


def recipe_list(request):
    recipes = Recipe.objects.filter(is_approved=True).order_by("category", "title")
    category = request.GET.get("category", "")
    categories = [c for c, _ in Recipe.CATEGORY_CHOICES]
    if category in categories:
        recipes = recipes.filter(category=category)
    else:
        category = ""
    return render(request, "recipes/list.html", {
        "recipes": recipes,
        "categories": categories,
        "current": category,
    })


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.is_approved = request.user.is_staff
            recipe.save()
            if request.user.is_staff:
                messages.success(request, "Recipe added!")
            else:
                messages.success(request, "Recipe submitted!")
            return redirect("recipe_list")
    else:
        form = RecipeForm()
    return render(request, "recipes/form.html", {"form": form})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, is_approved=True)
    return render(request, "recipes/detail.html", {"recipe": recipe})


def current_monday():
    today = date.today()
    return today - timedelta(days=today.weekday())


@login_required
def weekly_planner(request):
    monday = current_monday()
    if request.method == "POST":
        form = MealPlanForm(request.POST)
        if form.is_valid():
            MealPlan.objects.update_or_create(
                user=request.user,
                day=form.cleaned_data["day"],
                meal_type=form.cleaned_data["meal_type"],
                week_start=monday,
                defaults={"recipe": form.cleaned_data["recipe"]},
            )
            messages.success(request, "Meal saved to your weekly plan.")
            return redirect("weekly_planner")
    else:
        form = MealPlanForm()
    plans = MealPlan.objects.filter(user=request.user, week_start=monday).select_related("recipe")
    plan_map = {f"{p.day}|{p.meal_type}": p for p in plans}
    rows = []
    for d in DAYS:
        cells = []
        for m in MEALS:
            cells.append({"meal": m, "plan": plan_map.get(f"{d}|{m}")})
        rows.append({"day": d, "cells": cells})
    return render(request, "planner/weekly.html", {
        "form": form,
        "meals": MEALS,
        "rows": rows,
        "week_start": monday,
    })


@login_required
@require_POST
def delete_meal(request, pk):
    get_object_or_404(MealPlan, pk=pk, user=request.user).delete()
    messages.success(request, "Meal removed.")
    return redirect("weekly_planner")


def split_ingredients(text):
    items = []
    for line in text.splitlines():
        for part in re.split(r",\s*(?![^()]*\))", line):
            part = part.strip(" .")
            if part:
                items.append(part[0].upper() + part[1:])
    return items


@login_required
def grocery_list(request):
    monday = current_monday()
    plans = MealPlan.objects.filter(user=request.user, week_start=monday).select_related("recipe")
    groups = OrderedDict()
    ordered = sorted(plans, key=lambda p: (DAYS.index(p.day), MEALS.index(p.meal_type)))
    for plan in ordered:
        if plan.recipe_id not in groups:
            groups[plan.recipe_id] = {
                "recipe": plan.recipe,
                "slots": [],
                "items": split_ingredients(plan.recipe.ingredients),
            }
        groups[plan.recipe_id]["slots"].append(f"{plan.day} {plan.meal_type}")
    return render(request, "planner/groceries.html", {
        "groups": list(groups.values()),
        "week_start": monday,
    })