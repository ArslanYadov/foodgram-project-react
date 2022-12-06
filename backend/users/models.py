from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    """Класс менджера пользователя."""
    def _create_user(
        self,
        first_name,
        last_name,
        username,
        email,
        password, 
        **kwargs
    ):
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(
        self,
        first_name,
        last_name,
        username,
        email,
        password
    ):
        return self._create_user(
            first_name,
            last_name,
            username,
            email,
            password  
        )

    def create_superuser(
        self,
        first_name,
        last_name,
        username,
        email,
        password
    ):
        return self._create_user(
            first_name,
            last_name,
            username,
            email,
            password,
            is_staff=True,
            is_superuser=True
        )


class User(AbstractUser, PermissionsMixin):
    """Модель пользователя."""
    username = models.CharField(
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
