from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmountForRecipe,
    Recipe,
    ShoppingCart,
    Tag
)
from rest_framework import serializers
from users.serializers import UserDetailSerializer
from api.utils import Base64ImageField


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
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('ingredients', 'is_favorited', 'is_in_shopping_cart')
    
    def get_ingredients(self, obj):
        queryset = obj.ingredient_amount.all()
        return IngredientAmountForRecipeSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return obj.favorite_recipe.exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return obj.recipe_in_cart.exists()


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для методов POST, PATCH и DEL."""
    ingredients = IngredientAmountForRecipeSerializer()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'coocking_time'
        )

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientAmountForRecipe.objects.get_or_create(
                recipe=recipe,
                ingredients=ingredient.get('ingredient'),
                amount=ingredient.get('amount')
            )
        return recipe


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов."""
    
    class Meta:
        model = Favorite
        fields = '__all__'

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        recipe = attrs.get('recipe')
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Данный рецепт уже добавлен в избранное.')
        return attrs


class ShoppingCart(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""
    
    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        recipe = attrs.get('recipe')
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Данный рецепт уже добавлен в список покупок.')
        return attrs
