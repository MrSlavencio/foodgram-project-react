# Generated by Django 4.1.6 on 2023-02-16 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_ingredientsinreciepe_ingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reciepe',
            name='created',
        ),
    ]