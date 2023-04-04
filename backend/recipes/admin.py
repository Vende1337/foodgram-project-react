from django.contrib.admin import ModelAdmin, register, TabularInline
from django.core.exceptions import ValidationError

from .models import (Tag, Recipe, Favorite, Follow, Ingredient,
                     RecipeinIngredients, Purchase)


@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('user', 'author')


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)


class RecipeinIngredientsInline(TabularInline):
    model = RecipeinIngredients
    extra = 1


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    inlines = [RecipeinIngredientsInline]
    list_display = ('name', 'author', 'favorite')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name',)
    readonly_fields = ('favorite',)
    fields = ('image',
              ('name', 'author'),
              'text',
              ('tags', 'cooking_time'),
              'favorite')

    def favorite(self, obj):
        return obj.favorite.count()
    favorite.short_description = 'Кол-во добавлений в избранное'

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('text'):
            raise ValidationError('Поле "text" является обязательным')
        if not cleaned_data.get('ingredient_in_recipe').exists():
            raise ValidationError(
                'Необходимо добавить как минимум один ингредиент в рецепт')

    # def save_model(self, request, obj, form, change):
    #     if obj.ingredient_in_recipe.count() < 1:
    #         raise ValidationError(
    #             'Необходимо добавить как минимум один ингредиент в рецепт')
    #     super().save_model(request, obj, form, change)


@register(RecipeinIngredients)
class RecipeIngredientAdmin(ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('recipe', 'user')


@register(Purchase)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('recipe', 'user')
