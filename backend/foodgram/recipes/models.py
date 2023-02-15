from core.models import CreatedModel
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Unit(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='Полное название единицы измерения',
        help_text='Полное название единицы измерения'
    )
    short_name = models.CharField(
        max_length=8,
        unique=True,
        verbose_name='Единица измерения',
        help_text='Сокращенное название единицы измерения'
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.short_name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Ингредиент',
        help_text='Название ингредиента'
    )
    quantity = models.FloatField(
        verbose_name='Количество',
        help_text='Количество ингредиента'
    )
    unit = models.ForeignKey(
        Unit,
        related_name='unit',
        on_delete=models.CASCADE,
        verbose_name='Единица измерения',
        help_text='Единица измерения ингредиента'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Тег',
        help_text='Название тега'
    )
    hex_code = models.CharField(
        max_length=10,
        verbose_name='Цвет',
        help_text='Цветовой hex-код'
    )
    slug = models.SlugField(
        max_length=15,
        verbose_name='Слаг',
        help_text='Слаг тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Reciepe(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Автор рецепта'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipies/',
        null=True,
        blank=True,
        verbose_name='Картинка',
        help_text='Изображение рецепта'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        related_name='ingredients'
    )
    tag = models.ManyToManyField(
        to=Tag,
        related_name='tag'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name
