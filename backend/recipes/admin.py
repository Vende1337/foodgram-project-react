from django.contrib.admin import ModelAdmin, register, TabularInline

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


@register(RecipeinIngredients)
class RecipeIngredientAdmin(ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('recipe', 'user')


@register(Purchase)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('recipe', 'user')
