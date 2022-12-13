from django.contrib import admin
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmountForRecipe,
    Recipe,
    Tag
)


admin.site.register(Favorite)
admin.site.register(Ingredient)
admin.site.register(IngredientAmountForRecipe)
admin.site.register(Tag)
admin.site.register(Recipe)
