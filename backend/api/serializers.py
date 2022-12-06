from foodgram.settings import RESERVED_USERNAME_LIST
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
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
                {
                    'username': ('Данное имя зарезервированно!')
                }
            )

    def save(self, *args, **kwargs):
        user = User(
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            username=self.validated_data.get('username'),
            email=self.validated_data.get('email')
        )
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()
        return user
