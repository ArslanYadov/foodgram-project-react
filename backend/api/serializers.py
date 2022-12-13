from recipes.models import Ingredient, IngredientAmountForRecipe, Recipe, Tag
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
    author = UserDetailSerializer()
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'coocking_time'
        )
        read_only_fields = ('ingredients',)
    
    def get_ingredients(self, obj):
        queryset = IngredientAmountForRecipe.objects.filter(recipe=obj)
        return IngredientAmountForRecipeSerializer(queryset, many=True).data


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для методов POST, PATCH и DEL."""
    pass
