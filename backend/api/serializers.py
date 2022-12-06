from foodgram.settings import RESERVED_USERNAME_LIST
from users.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )
        model = User


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_username(self, value):
        if value.lower() in RESERVED_USERNAME_LIST:
            raise serializers.ValidationError(
                {
                    'username': ('Данное имя зарезервированно!')
                }
            )
        return value


class UserGetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=254)
