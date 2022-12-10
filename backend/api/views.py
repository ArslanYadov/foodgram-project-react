from api.serializers import IngredientSerializer, TagSerializer
from recipes.models import Ingredient, Tag
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet


class IngredientViewSet(ReadOnlyModelViewSet):
    """Отображение ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (SearchFilter,)
    search_fields = ('$name',)


class TagViewSet(ReadOnlyModelViewSet):
    """Отображение всех тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
