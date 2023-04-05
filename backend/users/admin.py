from django.contrib.admin import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import User


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name',)


@register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # add_form = CustomUserCreationForm
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email', 'first_name', 'last_name',),
    #     }),
    # )
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
