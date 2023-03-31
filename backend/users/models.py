from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

from users.validate import validate_username


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_username],
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        validators=[
            RegexValidator(
                r"^[а-яА-Яa-zA-Z]+$",
                message="Имя может содержать только буквы",
            )
        ],
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=False,
        validators=[
            RegexValidator(
                r"^[а-яА-Яa-zA-Z]+$",
                message="Фамилия может содержать только буквы",
            )
        ],
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        "username",
        "first_name",
        "last_name",
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


