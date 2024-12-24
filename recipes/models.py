from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название ингредиента')

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название рецепта')
    description = models.TextField(verbose_name='Описание')
    steps = models.TextField(verbose_name='Шаги приготовления')
    cooking_time = models.PositiveIntegerField(verbose_name='Время приготовления (в минутах)')
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True, verbose_name='Изображение рецепта')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор')
    categories = models.ManyToManyField(Category, through='RecipeCategory', verbose_name='Категории')
    ingredients = models.ManyToManyField(Ingredient, blank=True, verbose_name='Ингредиенты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f"{self.recipe.title} -> {self.category.name}"