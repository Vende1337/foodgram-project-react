from django_filters import rest_framework as filters, CharFilter

from recipes.models import Recipe, Ingredient


class RecipeFilter(filters.FilterSet):
    """Фильтр для рецептов"""

    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart', ]

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(purchase__user=self.request.user)
        return queryset


class IngredientFilter(filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)
