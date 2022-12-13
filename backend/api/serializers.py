from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmountForRecipe,
    Recipe,
    Tag
)
from rest_framework import serializers
from users.serializers import UserDetailSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов."""

    class Meta:
        model = Tag
        fields = '__all__'
    

class IngredientAmountForRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов с количеством."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmountForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipesListSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для метода GET."""
    tags = TagSerializer(many=True)
    author = UserDetailSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('ingredients', 'is_favorited')
    
    def get_ingredients(self, obj):
        queryset = IngredientAmountForRecipe.objects.filter(recipe=obj)
        return IngredientAmountForRecipeSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для методов POST, PATCH и DEL."""
    pass


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов."""
    
    class Meta:
        model = Favorite
        fields = '__all__'
    
    def validate(self, data):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        recipe = data.get('recipe')
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Данный рецепт уже добавлен в избранное.')
        return data
