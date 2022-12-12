from django.contrib import admin
from recipes.models import Ingredient, IngredientAmountForRecipe, Recipe, Tag

admin.site.register(Ingredient)
admin.site.register(IngredientAmountForRecipe)
admin.site.register(Tag)
admin.site.register(Recipe)
