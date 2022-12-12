from api.serializers import IngredientSerializer, RecipesListSerializer, TagSerializer
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import filters, viewsets, permissions


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Отображение ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Отображение всех тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Отображение рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author__username', 'tags__slug')

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return RecipesListSerializer
