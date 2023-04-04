from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

from users.validate import validate_username, validate_character_field
from api_foodgram.settings import MAX_LEN_NAME, MAX_LEN_EMAIL


class User(AbstractUser):
    username = models.CharField(
        max_length=MAX_LEN_NAME,
        unique=True,
        validators=[UnicodeUsernameValidator(), validate_username],
    )
    email = models.EmailField(
        max_length=MAX_LEN_EMAIL,
        unique=True,
    )
    first_name = models.CharField(
        max_length=MAX_LEN_NAME,
        blank=False
        null=False,
        validators=[validate_character_field],
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=MAX_LEN_NAME,
        blank=False,
        null=False,
        validators=[validate_character_field],
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
