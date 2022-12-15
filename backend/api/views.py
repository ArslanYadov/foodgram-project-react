from api.permissions import IsAuthorAdminModerOrReadOnly
from api.serializers import (
    IngredientSerializer,
    FavoriteSerializer,
    RecipesListSerializer,
    RecipeSerializer,
    TagSerializer
)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, Tag
from rest_framework import filters, viewsets, permissions, response, status
from rest_framework.decorators import action


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
    permission_classes = (IsAuthorAdminModerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author__username', 'tags__slug')

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return RecipesListSerializer
        return RecipeSerializer

    @action(
        methods=['POST'], detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavoriteSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        obj = get_object_or_404(klass=Favorite, user=user, recipe=recipe)
        obj.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
