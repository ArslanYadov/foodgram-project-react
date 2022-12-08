from api.serializers import TagSerializer
from recipes.models import Tag
from rest_framework.viewsets import ReadOnlyModelViewSet

class TagViewSet(ReadOnlyModelViewSet):
    """Отображение всех тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
