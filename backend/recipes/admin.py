from django.contrib import admin
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmountForRecipe,
    Recipe,
    ShoppingCart,
    Tag
)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Класс админки избранного."""
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Класс админки ингредиентов."""
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )


@admin.register(IngredientAmountForRecipe)
class IngredientAmountForRecipeAdmin(admin.ModelAdmin):
    """Класс админки для количества ингредиента в рецепте."""
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe', )
    search_fields = ('ingredient__name', 'recipe__name')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Класс админки рецептов."""
    list_display = ('name', 'author', 'amount_favorite')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('author__username', 'name__icontains')

    @admin.display(description='Количество в избранном')
    def amount_favorite(self, obj):
        amount = Favorite.objects.filter(recipe=obj).count()
        return amount


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Класс админки списка покупок."""
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Класс админки тэгов."""
    list_display = ('slug', )
    list_filter = ('slug', )
    search_fields = ('slug', )
