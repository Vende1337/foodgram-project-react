# Generated by Django 4.1.7 on 2023-04-03 16:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='unit',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(default=1, max_length=75),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[а-яА-Яa-zA-Z\\s]+$', message='Поле может содержать только буквы')], verbose_name='Название Ингридиент'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(verbose_name='Время приготовления в минутах'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator('^[а-яА-Яa-zA-Z\\s]+$', message='Поле может содержать только буквы')], verbose_name='Название рецепта'),
        ),
        migrations.AlterField(
            model_name='recipeiningredients',
            name='amount',
            field=models.PositiveSmallIntegerField(verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipeiningredients',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipes.ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeiningredients',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_in_recipe', to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[а-яА-Яa-zA-Z\\s]+$', message='Поле может содержать только буквы')], verbose_name='Название Тега'),
        ),
    ]