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
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

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
        read_only_fields = (
            'ingredients', 'is_favorited', 'is_in_shopping_cart'
        )

    def get_ingredients(self, obj):
        queryset = obj.ingredient_amount.all()
        return IngredientAmountForRecipeSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return user.favorite_recipe.exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return user.recipe_in_cart.exists()


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для методов POST, PATCH."""
    ingredients = IngredientAmountForRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def validate(self, attrs):
        ingredients = self.initial_data.get('ingredients')
        validated_ingrediets = []
        unique_ingredients_id = []
        for ingredient in ingredients:
            ingredient_id = ingredient.get('id')
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError({
                    'ingredient_id': (
                        'Не существующий ингредиент: {}'.format(ingredient_id)
                    )
                })

            if ingredient_id in unique_ingredients_id:
                raise serializers.ValidationError({
                    'ingredient_id': (
                        'Ингредиенты не должны повторяться.'
                    )
                })
            unique_ingredients_id.append(ingredient_id)

            amount = ingredient.get('amount')
            validated_ingrediets.append(
                {'id': ingredient_id, 'amount': amount}
            )

        attrs['ingredients'] = validated_ingrediets
        return attrs

    def _set_amount_to_ingredient(self, recipe, ingredients):
        for ingredient in ingredients:
            IngredientAmountForRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self._set_amount_to_ingredient(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        recipe = instance
        recipe.image = validated_data.get(
            'image', recipe.image
        )
        recipe.name = validated_data.get(
            'name', recipe.name
        )
        recipe.text = validated_data.get(
            'text', recipe.text
        )
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time
        )

        tags = validated_data.get('tags')
        ingredients = validated_data.get('ingredients')
        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)
        if ingredients:
            recipe.ingredients.clear()
            self._set_amount_to_ingredient(recipe, ingredients)

        recipe.save()
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipesListSerializer(instance, context=context).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения рецепта с меньшим кол-вом полей.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов."""

    class Meta:
        model = Favorite
        fields = '__all__'

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        if user.favorite_recipe.exists():
            raise serializers.ValidationError(
                {'error': 'Данный рецепт уже добавлен в избранное.'}
            )
        return attrs

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        if user.recipe_in_cart.exists():
            raise serializers.ValidationError(
                {'error': 'Данный рецепт уже добавлен в список покупок.'}
            )
        return attrs

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': request}
        ).data
