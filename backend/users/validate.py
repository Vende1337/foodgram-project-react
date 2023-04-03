from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_username(username):
    if len(username) < 3:
        raise ValidationError("Логин должен быть содержать минимум 3 символа")


validate_character_field = RegexValidator(
    r"^[а-яА-Яa-zA-Z\s]+$",
    message="Поле может содержать только буквы",
)
