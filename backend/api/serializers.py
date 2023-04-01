from django.db import transaction
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User
from recipes.models import Tag, Ingredient, Recipe, RecipeinIngredients, Follow, Purchase, Favorite


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей Djoiser"""
    is_subscribed = serializers.SerializerMethodField(default=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, user):
        if self.context.get('request').user.is_authenticated:
            return user.following.filter(
                user=self.context.get('request').user, author=user.id
            ).exists()
        return False


class GetIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'unit', ]


class RecipeIngred(serializers.ModelSerializer):
    """Сериализатор для ингредиентов при создании рецепта"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredients'
    )

    class Meta:
        model = RecipeinIngredients
        fields = ['id', 'amount', ]


class GetTagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'color', ]


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецепта(короткий)"""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['id',
                  'name', 'image', 'cooking_time']


class GetRecipeIngredient(serializers.ModelSerializer):
    """Сериализатор для получения ингредиента в рецепте"""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    unit = serializers.ReadOnlyField(
        source='ingredient.unit'
    )

    class Meta:
        model = RecipeinIngredients
        fields = ['id', 'name', 'unit', 'amount']


class GetRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для получения рецепта"""

    ingredients = GetRecipeIngredient(
        many=True, read_only=True, source='ingredient_in_recipe')

    author = UsersSerializer()

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
    """Сериализатор для создания рецепта"""

    ingredients = RecipeIngred(many=True)

    author = UsersSerializer(default=serializers.CurrentUserDefault())

    image = Base64ImageField()

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'author', 'image', 'ingredients', 'tags',
                  'name', 'text', 'cooking_time', ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)
            RecipeinIngredients.objects.bulk_create(
                [RecipeinIngredients(
                    recipe=recipe,
                    ingredient=ingredient['ingredients'],
                    amount=ingredient['amount']
                ) for ingredient in ingredients_data]
            )
            recipe.tags.set(tags_data)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        RecipeinIngredients.objects.filter(recipe=instance).delete()
        recipe_ingredients = [
            RecipeinIngredients(
                recipe=instance,
                ingredient=ingredient.get('ingredients'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients
        ]
        with transaction.atomic():
            RecipeinIngredients.objects.bulk_create(recipe_ingredients)
        instance.tags.set(tags)
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        return instance

    def to_representation(self, instance):

        res = GetRecipeSerializer(instance, context=self.context)

        return res.data


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""

    class Meta:
        model = Follow
        fields = ['user', 'author']
        read_only_fields = ('user', 'author',)

    def validate(self, data):
        user, author = data.get('user'), data.get('author')
        if Follow.objects.filter(user=user, author=author).exists():
            raise ValidationError(
                {'error': 'Вы уже подписаны на этого пользователя'}
            )
        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка подписок"""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name',
                  'last_name', 'id', 'is_subscribed', 'recipes', 'recipes_count']

    def get_is_subscribed(self, user):
        if self.context.get('request').user.is_authenticated:
            return user.following.filter(
                user=self.context["request"].user, author=user.pk
            ).exists()
        return False

    def get_recipes(self, user):
        recipes = user.recipes.all()
        res = []

        for recipe in recipes:
            res.append(ShortRecipeSerializer(recipe).data)
        return res

    def get_recipes_count(self, user):
        return user.recipes.all().count()
