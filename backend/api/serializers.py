from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
import webcolors
from rest_framework.response import Response
from djoser.serializers import UserCreateSerializer, UserSerializer as JSUser

from users.models import User

from recipes.models import Tag, Ingredient, Recipe, RecipeinIngred, Follow, Purchase, Favorite





class CustomUserRegisterSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей Djoiser"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name',
                  'last_name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name',
                  'last_name', 'password', 'id', ]
        

class CustomUserSerializer(JSUser):
    """Сериализатор для пользователей Djoiser"""
    is_subscribed = serializers.SerializerMethodField(default=True)

   

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed')       


    def get_is_subscribed(self, user):
        self_user = self.context.get('request').user.id
        if self_user == user:
            return False
        if Follow.objects.filter(user=self_user, author=user).exists():
            return True
        return False
     


class SelfUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name',
                  'last_name', 'id', 'is_subscribed', ]

    def get_is_subscribed(self, user):
        self_user = self.context.get('request').user.id
        if self_user == user:
            return False
        if Follow.objects.filter(user=self_user, author=user).exists():
            return True
        return False


class SetPassSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()
    current_serializer = serializers.CharField()


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'password',
            'email',
        ]


class GetIngresientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'unit', ]


class Recipeingred(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredients'
    )

    class Meta:
        model = RecipeinIngred
        fields = ['id', 'amount', ]


class GetTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'color', ]


class ShortRecipeSerializer(serializers.ModelSerializer):

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['id',
                  'name', 'image', 'cooking_time']


class GetRecipeIngred(serializers.ModelSerializer):

    id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id',
        source='ingredient'
    )
    name = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        source='ingredient'
    )
    unit = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id',
        source='ingredient'
    )

    class Meta:
        model = RecipeinIngred
        fields = ['id', 'name', 'unit', 'amount']


class GetRecipeSerializer(serializers.ModelSerializer):

    ingredients = GetRecipeIngred(
        many=True, read_only=True, source='ingred_in_recipe')

    author = SelfUserSerializer()

    image = Base64ImageField()

    tags = GetTagSerializer(many=True, read_only=True)

    is_favorited = serializers.SerializerMethodField()

    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'author', 'image', 'ingredients', 'tags',
                  'name', 'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, recipe):
        self_user = self.context.get('request').user.id
        if Favorite.objects.filter(user=self_user, recipe=recipe).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        self_user = self.context.get('request').user.id
        if Purchase.objects.filter(user=self_user, recipe=recipe).exists():
            return True
        return False


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = Recipeingred(many=True)

    author = SelfUserSerializer(default=serializers.CurrentUserDefault())

    image = Base64ImageField()

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'author', 'image', 'ingredients', 'tags',
                  'name', 'text', 'cooking_time', ]

    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:

            RecipeinIngred.objects.create(recipe=recipe, ingredient=ingredients[0].get(
                'ingredients'), amount=ingredient.get('amount'))
        recipe.tags.set(tags)

        recipe.save()

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        ingr = []
        RecipeinIngred.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            RecipeinIngred.objects.create(recipe=instance, ingredient=ingredient.get(
                'ingredients'), amount=ingredient.get('amount'))
            ingr.append(ingredient.get('ingredients').id)
        instance.tags.set(tags)
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.ingredients.set(ingr)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        return instance

    def to_representation(self, instance):

        res = GetRecipeSerializer(instance, context=self.context)

        return res.data


class FallowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['user', 'author']
        read_only_fields = ('user', 'author',)


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name',
                  'last_name', 'id', 'is_subscribed', 'recipes', 'recipes_count']

    def get_is_subscribed(self, user):
        self_user = self.context.get('request').user.id
        if self_user == user:
            return False
        if Follow.objects.filter(user=self_user, author=user).exists():
            return True
        return False

    def get_recipes(self, user):
        recipes = user.recipes.all()
        res = []

        for recipe in recipes:
            res.append(ShortRecipeSerializer(recipe).data)
        return res

    def get_recipes_count(self, user):
        recipes = user.recipes.all()
        count = 0
        for recipe in recipes:
            count += 1

        return count
