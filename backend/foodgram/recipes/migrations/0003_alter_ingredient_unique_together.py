# Generated by Django 4.1.6 on 2023-02-16 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_remove_ingredient_quantity_ingredientsinreciepe_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ingredient',
            unique_together={('name', 'unit')},
        ),
    ]