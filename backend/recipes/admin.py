from django.contrib import admin

from .models import Tag, Recipe, Favorite, Follow, Ingredient, RecipeinIngred, Purchase

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Ingredient)
admin.site.register(RecipeinIngred)
admin.site.register(Purchase)