from django.contrib.admin import ModelAdmin, register

from .models import Tag, Recipe, Favorite, Follow, Ingredient, RecipeinIngred, Purchase



@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('name', 'unit')
  

@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name',)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author',  'favorite')
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


@register(RecipeinIngred)
class RecipeIngredientAdmin(ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('recipe', 'user')


@register(Purchase)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('recipe', 'user')
