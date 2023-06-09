from django.urls import include, path
from rest_framework import routers

from .views import (
    UserViewSet,
    TagsViewSet,
    RecipesViewSet,
    IngredientViewSet,
    FollowViewSet,
    FavoriteViewSet,
    PurchaseViewSet,
)


router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='user-create')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('recipes', RecipesViewSet, basename='recipe')
router_v1.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                   FavoriteViewSet, basename='favorite')
router_v1.register('ingredients', IngredientViewSet, basename='ingredient')
router_v1.register(r'users/(?P<user_id>\d+)/subscribe',
                   FollowViewSet, basename='subscribe')
router_v1.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                   PurchaseViewSet, basename='purchase')


urlpatterns = [
    path('api/', include(router_v1.urls)),
]
