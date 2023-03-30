import mimetypes
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import reportlab
import pdfkit
from django.shortcuts import render
from rest_framework import viewsets, status, permissions, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import action, parser_classes
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
import json
from rest_framework.parsers import FileUploadParser
from .serializers import SelfUserSerializer, UserSerializer, SetPassSerializer, TokenSerializer,CustomUserSerializer, GetTagSerializer, RecipeSerializer, FallowSerializer, GetIngresientSerializer, GetRecipeSerializer, SubscriptionSerializer, ShortRecipeSerializer
from users.models import User
from recipes.models import Tag, Recipe, Favorite, Ingredient, Follow, Purchase, RecipeinIngred
from .permissions import IsAdminOrReadOnly, UserPermission,IsReviewAndComment
from.mixins import CreateDestroyViewSet
from .filters import MyFilter
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as JSViewSet
class UserViewSet(JSViewSet):
    queryset = User.objects.all()
    search_fields = ('=username',)
    permission_classes = (permissions.AllowAny,)
    serializer_class= CustomUserSerializer

    # def get_serializer_class(self):
    #     if self.request.user.is_staff:
    #         return SelfUserSerializer
    #     if self.request.method == 'GET':
    #         return SelfUserSerializer
    #     return CustomUserSerializer

    # @action(
    #     detail=False,
    #     url_path='me',
    #     permission_classes=(permissions.IsAuthenticated,)
    # )
    # def self_user(self, request):
    #     user = self.request.user
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)
    
    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions'

    )
    def gssset_queryset(self,request):
        user = request.user
        follows = User.objects.filter(following__user=user)
        page = self.paginate_queryset(follows)
        serializer = SubscriptionSerializer(
            page, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)


class SetPasswordViewSet(generics.GenericAPIView):
    serializer_class = SetPassSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, serializer):
        user = self.request.user
        new_pass = serializer.data.get('new_password')
        cur_pass = serializer.data.get('current_password')
        if not user.check_password(cur_pass):
            return Response({'error': 'Вы ввели неверный текущий пароль'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_pass)
        user.save()
        return Response(status=status.HTTP_200_OK)



class TagsViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = GetTagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer
    permission_classes = (IsReviewAndComment,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MyFilter

 

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return RecipeSerializer

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart'

    )
    def lisst(self, request):
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
    @action(
        detail=False,
        methods=['get'],
        url_path='favorsasdite'
    )
    def getdddd_queryset(self,request):
        user = request.user
        print(request)
        fav = Recipe.objects.filter(favorite__user=user)
        print(fav)
        page = self.paginate_queryset(fav)
        serializer = GetRecipeSerializer(
            page, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)




class FallowViewSet(CreateDestroyViewSet):
    serializer_class = FallowSerializer
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


class GetFallowViewSet(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions'

    )
    def get_queryset(self):
        fal = Follow.objects.filter(user=self.request.user)
        user = []
        for f in fal:
            user.append(f.author)
        print(user)    
        return user


class IngridientViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = GetIngresientSerializer
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


class PurchaseOutPDFViewSet(viewsets.ModelViewSet):
    serializer_class = ShortRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Purchase.objects.all()

    @ action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart'

    )
    def lisst(self, request):
        print(111111)
        recipe = Purchase.objects.filter(user=self.request.user).all()
        serializer = ShortRecipeSerializer(recipe)
        print(recipe)
        return Response(serializer.data)
