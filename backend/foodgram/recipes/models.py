# from core.models import CreatedModel
from django.contrib.auth import get_user_model
from django.db import models

from django.core.validators import MinValueValidator
from django.db.models import CheckConstraint, Q

from users.models import User
#User = get_user_model()



class Unit(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Полное название единицы измерения',
        help_text='Полное название единицы измерения'
    )
    short_name = models.CharField(
        max_length=200,
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
        max_length=200,
        verbose_name='Ингредиент',
        help_text='Название ингредиента'
    )
    measurement_unit = models.ForeignKey(
        Unit,
        related_name='unit',
        on_delete=models.CASCADE,
        verbose_name='Единица измерения',
        help_text='Единица измерения ингредиента'
    )
    
    class Meta:
        unique_together = ('name', 'measurement_unit',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        ingr_unit = f'{self.name}, {self.measurement_unit}'
        return ingr_unit
    

class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        #related_name='ingredienting',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        help_text='Ингредиенты'
    )
    reciepe = models.ForeignKey(
        'Reciepe',
        related_name='ingredientrec',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Рецепт'
    )
    amount = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name='Количество',
        help_text='Количество ингредиента'
    )

    class Meta:
        constraints = (
            CheckConstraint(
                check=Q(amount__gte=0.0),
                name='amount is non-negative'),
            )
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        ingr_qut_unit = f'{self.ingredient.name} - {self.amount}, {self.ingredient.measurement_unit}'
        return ingr_qut_unit
    

class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Тег',
        help_text='Название тега'
    )
    hex_code = models.CharField(
        max_length=7,
        verbose_name='Цвет',
        help_text='Цветовой hex-код'
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг',
        help_text='Слаг тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class TagReciepe(models.Model):
    tag = models.ForeignKey(
        Tag,
        related_name='tag_name',
        on_delete=models.CASCADE,
        verbose_name='Тег',
        help_text='Тег рецепта'
    )
    reciepe = models.ForeignKey(
        'Reciepe',
        related_name='tag_reciepe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Рецепт'
    )
    
    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'

    def __str__(self):
        return f'{self.tag}_{self.reciepe}'
    

class Reciepe(models.Model):
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
        Ingredient,
        through=IngredientAmount,
        verbose_name='Ингредиенты',
        help_text='Ингредиенты рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        through=TagReciepe,
        related_name='reciepe_tag',
        verbose_name='Теги',
        help_text='Теги рецепта'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах',
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name
    
    
class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
        help_text='Пользователь, который подписывается'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор',
        help_text='Пользователь, на которого подписываются'
    )


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Reciepe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
        help_text='Рецепт в избранном'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Пользователь',
        help_text='Пользователь, добавивший рецепт в избранное'
    )
    adding_dt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-adding_dt']
        verbose_name = 'Избранное'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} added {self.recipe}'
    
    
class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Reciepe,
        on_delete=models.CASCADE,
        related_name='in_shoppingcard',
        verbose_name='Рецепт',
        help_text='Рецепт в список покупок'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='in_shoppincard_user',
        verbose_name='Пользователь',
        help_text='Пользователь, добавивший рецепт в список покупок'
    )
    adding_dt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-adding_dt']
        verbose_name = 'Список покупок'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user} added {self.recipe}"