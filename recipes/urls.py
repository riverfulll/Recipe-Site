from django.urls import path
from .views import (
    index_view, recipe_detail_view,
    register_view, login_view, logout_view,
    recipe_add_view, recipe_edit_view
)

urlpatterns = [
    path('', index_view, name='index'),
    path('recipe/<int:recipe_id>/', recipe_detail_view, name='recipe_detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('recipe/add/', recipe_add_view, name='recipe_add'),
    path('recipe/<int:recipe_id>/edit/', recipe_edit_view, name='recipe_edit'),
]