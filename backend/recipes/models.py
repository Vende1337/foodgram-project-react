from django.db import models
from colorfield.fields import ColorField
from users.models import User


class Ingredient(models.Model):

    UNITS = [
        ('kg', 'Кг.'),
        ('gramm', 'Грамм'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name='Название Ингридиент',
    )
    unit = models.CharField(max_length=20, choices=UNITS, default='gramm')

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название Тега',
    )

    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Идентификатор Тега',
    )

    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )

    image = models.ImageField()

    text = models.TextField(
        max_length=1500,
        blank=True,
        verbose_name='Описание',
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeinIngred',
        related_name='ingredients',
        verbose_name='Ингридиент'
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        null=False,
        verbose_name='Тег'
    )

    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах',
    )

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_cannot_follow_yourself'
            ),
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='nonunique_following_constraint'
            )
        ]


class RecipeinIngred(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingred_in_recipe')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredient')
    amount = models.IntegerField(
        verbose_name='Количество'
    )


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+',)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorite',)

    class Meta:
        unique_together = ('user', 'recipe')


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,related_name='purchase')

    class Meta:
        unique_together = ('user', 'recipe')
