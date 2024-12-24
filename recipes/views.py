import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe, Category, Ingredient
from .forms import CustomUserCreationForm, CustomAuthenticationForm, RecipeForm

def index_view(request):
    category_id = request.GET.get('category') 
    if category_id:
        recipes = Recipe.objects.filter(categories__id=category_id) 
    else:
        recipes = Recipe.objects.all()

    categories = Category.objects.all()
    context = {
        'recipes': recipes,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None, 
    }
    return render(request, 'index.html', context)

def recipe_detail_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    categories = recipe.categories.all()
    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'categories': categories,
    })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Добро пожаловать!')
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('index')

@login_required
def recipe_add_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            new_categories = form.cleaned_data.get('new_categories', '')
            if new_categories:
                for category_name in new_categories.split(','):
                    category_name = category_name.strip()
                    if category_name:
                        category, created = Category.objects.get_or_create(name=category_name)
                        recipe.categories.add(category)

            ingredients = form.cleaned_data.get('ingredients', '')
            if ingredients:
                for ingredient_name in ingredients.split(','):
                    ingredient_name = ingredient_name.strip()
                    if ingredient_name:
                        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
                        recipe.ingredients.add(ingredient)

            messages.success(request, 'Рецепт успешно добавлен!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()

    return render(request, 'recipe_form.html', {'form': form, 'title': 'Добавить рецепт'})

@login_required
def recipe_edit_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        messages.error(request, 'У вас нет прав на редактирование этого рецепта.')
        return redirect('recipe_detail', recipe_id=recipe.id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save()

            new_categories = form.cleaned_data.get('new_categories', '')
            if new_categories:
                for category_name in new_categories.split(','):
                    category_name = category_name.strip()
                    if category_name:
                        category, created = Category.objects.get_or_create(name=category_name)
                        recipe.categories.add(category)

            ingredients = form.cleaned_data.get('ingredients', '')
            recipe.ingredients.clear() 
            if ingredients:
                for ingredient_name in ingredients.split(','):
                    ingredient_name = ingredient_name.strip()
                    if ingredient_name:
                        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
                        recipe.ingredients.add(ingredient)

            messages.success(request, 'Рецепт успешно обновлён!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipe_form.html', {'form': form, 'title': 'Редактировать рецепт'})