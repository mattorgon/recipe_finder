from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

@csrf_exempt
def search_recipes_by_ingredients(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ingredients = data.get('ingredients')
        api_key = settings.SPOONACULAR_API_KEY
        
        # Fetch basic recipe information
        basic_response = requests.get(
            f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=10&limitLicense=true&ranking=1&ignorePantry=false&apiKey={api_key}'
        )
        basic_recipes = basic_response.json()
        
        detailed_recipes = []
        
        for recipe in basic_recipes:
            recipe_id = recipe['id']
            detailed_response = requests.get(
                f'https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=false&apiKey={api_key}'
            )
            detailed_info = detailed_response.json()
            recipe['spoonacularSourceUrl'] = detailed_info.get('spoonacularSourceUrl')
            recipe['readyInMinutes'] = detailed_info.get('readyInMinutes')
            detailed_recipes.append(recipe)
        
        return JsonResponse(detailed_recipes, safe=False)