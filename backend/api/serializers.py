from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers
from users.serializers import UserDetailSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class RecipesListSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'coocking_time'
        )