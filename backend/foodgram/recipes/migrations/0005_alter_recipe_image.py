# Generated by Django 4.1.6 on 2023-02-28 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_add_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(help_text='Изображение рецепта', upload_to='recipes/', verbose_name='Картинка'),
        ),
    ]
