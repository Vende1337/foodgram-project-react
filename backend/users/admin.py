from django.contrib.admin import register
from django.contrib import admin

from .models import User


@register(User)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
