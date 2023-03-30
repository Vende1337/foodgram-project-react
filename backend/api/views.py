from djoser.views import UserViewSet as DJUserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .filters import RecipeFilter
from .serializers import CustomUserSerializer, GetTagSerializer, RecipeSerializer, FollowSerializer, GetIngredientSerializer, GetRecipeSerializer, SubscriptionSerializer, ShortRecipeSerializer
from users.models import User
from recipes.models import Tag, Recipe, Favorite, Ingredient, Follow, Purchase, RecipeinIngred
from .permissions import IsAdminOrReadOnly, IsReviewAndComment
from .mixins import CreateDestroyViewSet


class UserViewSet(DJUserViewSet):
    queryset = User.objects.all()
    search_fields = ('=username',)
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions'

    )
    def subscriptions(self, request):
        user = request.user
        follows = User.objects.filter(following__user=user)
        page = self.paginate_queryset(follows)
        serializer = SubscriptionSerializer(
            page, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)


class TagsViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = GetTagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsReviewAndComment,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return RecipeSerializer

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart'

    )
    def download_shopping_cart(self, request):
        recipe = Purchase.objects.filter(user=self.request.user).all()
        res = {}
        for r in recipe:
            recipe = r.recipe
            rec_in_ingred = RecipeinIngred.objects.filter(recipe=r.recipe)
            for ingred in rec_in_ingred:
                ingredient = ingred.ingredient
                unit = ingred.ingredient.unit
                amount = ingred.amount
                if f'{ingredient},{unit} - ' in res:
                    cur_amount = res.get(
                        f'{ingredient},{unit} - ')
                    new_amount = int(cur_amount) + int(amount)
                    res[f'{ingredient},{unit} - '] = (str(new_amount))
                else:
                    res[f'{ingredient},{unit} - '] = (
                        str(amount))
        return HttpResponse('\n'.join(f'{key + value}' for key, value in res.items()), content_type='text/plain')


class FallowViewSet(CreateDestroyViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def delete(self, request, user_id):
        print(self.kwargs)
        print(user_id)
        follow = get_object_or_404(
            Follow, user=self.request.user, author=user_id)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, request):
        author = get_object_or_404(User, pk=self.kwargs['user_id'])
        new_follow = Follow.objects.create(
            user=self.request.user, author=author)
        new_follow.save()

        return Response(status=status.HTTP_201_CREATED)


class IngridientViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = GetIngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = ShortRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def delete(self, request, recipe_id):
        favorite = get_object_or_404(
            Favorite, user=self.request.user, recipe=recipe_id)
        favorite .delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, recipe_id):

        recipe = get_object_or_404(Recipe, pk=recipe_id)

        favorite = Favorite.objects.create(
            user=self.request.user, recipe=recipe)
        favorite.save()
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data)


class PurchaseViewSet(CreateDestroyViewSet):
    serializer_class = ShortRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)

    def delete(self, request, recipe_id):
        purchase = get_object_or_404(
            Purchase, user=self.request.user, recipe=recipe_id)
        purchase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, recipe_id):

        recipe = get_object_or_404(
            Recipe, pk=recipe_id)

        purchase = Purchase.objects.create(
            user=self.request.user, recipe=recipe)

        purchase.save()
        serializer = ShortRecipeSerializer(recipe)

        return Response(serializer.data)
