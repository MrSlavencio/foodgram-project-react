# Generated by Django 4.1.6 on 2023-02-22 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название ингредиента', max_length=200, verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(help_text='Количество ингредиента', verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецепте',
            },
        ),
        migrations.CreateModel(
            name='Reciepe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название рецепта', max_length=50, verbose_name='Название')),
                ('image', models.ImageField(blank=True, help_text='Изображение рецепта', null=True, upload_to='recipies/', verbose_name='Картинка')),
                ('description', models.TextField(help_text='Описание рецепта', verbose_name='Описание')),
                ('cooking_time', models.IntegerField(help_text='Время приготовления в минутах', verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название тега', max_length=200, verbose_name='Тег')),
                ('hex_code', models.CharField(help_text='Цветовой hex-код', max_length=7, verbose_name='Цвет')),
                ('slug', models.SlugField(help_text='Слаг тега', max_length=200, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Полное название единицы измерения', max_length=200, unique=True, verbose_name='Полное название единицы измерения')),
                ('short_name', models.CharField(help_text='Сокращенное название единицы измерения', max_length=200, unique=True, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
            },
        ),
        migrations.CreateModel(
            name='TagReciepe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reciepe', models.ForeignKey(help_text='Рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='tag_reciepe', to='recipes.reciepe', verbose_name='Рецепт')),
                ('tag', models.ForeignKey(help_text='Тег рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='tag_name', to='recipes.tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег рецепта',
                'verbose_name_plural': 'Теги рецепта',
            },
        ),
    ]
