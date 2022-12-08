from recipes.models import Tag
from rest_framework.serializers import ModelSerializer
from api.utils import Hex2NameColor

class TagSerializer(ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
