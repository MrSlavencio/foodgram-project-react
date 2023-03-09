import json
import os

from django.db import migrations

with open(os.path.join('data', 'ingredients.json'), 'r') as file:
    ingredients_json = file.read()

INITIAL_INGREDIENTS = json.loads(ingredients_json)


def add_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    for ingredient in INITIAL_INGREDIENTS:
        new_ingredient = Ingredient(**ingredient)
        new_ingredient.save()


def remove_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    for ingredient in INITIAL_INGREDIENTS:
        Ingredient.objects.get(name=ingredient['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_add_tags'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredients,
            remove_ingredients
        )
    ]
