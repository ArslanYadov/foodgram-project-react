import re
from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидация юзернейма."""
    match = re.search(r'^[\w.@+-]+\z', value)
    if not match:
        raise ValidationError(
            'Имя пользователя может содержать только латинские буквы, '
            'и символы [.@+-].'
        )
    return value
