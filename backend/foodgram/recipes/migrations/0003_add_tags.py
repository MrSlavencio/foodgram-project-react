from django.db import migrations

INITIAL_TAGS = [
    {'hex_code': '#F47835', 'name': 'Завтрак', 'slug': 'breakfast'},
    {'hex_code': '#1B8712', 'name': 'Обед', 'slug': 'lunch'},
    {'hex_code': '#FF9CCB', 'name': 'Ужин', 'slug': 'dinner'},
]


def add_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in INITIAL_TAGS:
        new_tag = Tag(**tag)
        new_tag.save()


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in INITIAL_TAGS:
        Tag.objects.get(name=tag['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_tags,
            remove_tags
        )
    ]
