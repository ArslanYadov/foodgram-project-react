from recipes.models import Tag
from rest_framework.serializers import ModelSerializer, ValidationError

class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
