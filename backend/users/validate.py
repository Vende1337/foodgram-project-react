import re

from django.core.exceptions import ValidationError


def validate_username(username):
    if len(username) < 3:
        raise ValidationError("Логин должен быть содержать минимум 3 символа")

    result = re.findall(r"[^\w-]", username)
    if result:
        raise ValidationError(
            f'Нельзя использовать \'{" ".join(_ for _ in set(result))}\' в логине'
        )
    return