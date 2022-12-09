from djoser.serializers import UserCreateSerializer, UserSerializer
from foodgram.settings import RESERVED_USERNAME_LIST
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Follow, User


class UserDetailSerializer(UserSerializer):
    """
    Переопределяем сериализатор для пользователя.
    Добавлено поле подписки, если имеется подписчики.
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return Follow.objects.filter(user=user, following=obj.id).exists()


class UserRegistrationSerializer(UserCreateSerializer):
    """
    Переопределяем регистрацию пользователя.
    Валидация по уникальности username и email.
    Валидация создания пользователя с username,
    который находится в зарезервированном списке.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email'],
            )
        ]

    def validate_username(self, value):
        if value.lower() in RESERVED_USERNAME_LIST:
            raise serializers.ValidationError(
                'Данное имя зарезервированно!'
            )
        return value


class FollowSerializer(UserDetailSerializer):
    """
    Сериализатор для подписок.
    Валидация по подписке на самого себя.
    Валидация по повторной подписке на автора.
    """
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    def validate_following(self, following):
        if self.context['request'].user == following:
            raise serializers.ValidationError(
                {
                    'follower': ('Нельзя подписаться на себя самого.')
                }
            )
        return following

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following',)
            )
        ]
