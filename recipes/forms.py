from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Recipe, Category, Ingredient

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Категории'
    )
    new_categories = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Добавить новые категории через запятую'}),
        label='Новые категории'
    )
    ingredients = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ингредиенты через запятую'}),
        label='Ингредиенты'
    )

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'steps', 'cooking_time', 'image', 'categories'
        ]
        labels = {
            'title': 'Название рецепта',
            'description': 'Описание',
            'steps': 'Шаги приготовления',
            'cooking_time': 'Время приготовления (в минутах)',
            'image': 'Изображение рецепта',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'steps': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }