from django.urls import path
from .views import search_recipes_by_ingredients

urlpatterns = [
    path('search_recipes_by_ingredients/', search_recipes_by_ingredients),
]