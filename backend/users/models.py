from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = models.CharField(
        max_length=150,
        unique=True,
        null=False,
        blank=False,
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
            'blank': 'Поле не может быть пустой строкой.',
            'null': 'Обязательное поле.'
        }
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        null=False,
        blank=False,
        error_messages={
            'unique': 'Пользователь с таким email уже существует.',
            'blank': 'Поле не может быть пустой строкой.',
            'null': 'Обязательное поле.'
        }
    )
    first_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        error_messages={
            'blank': 'Поле не может быть пустой строкой.',
            'null': 'Обязательное поле.'
        }
    )
    last_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        error_messages={
            'blank': 'Поле не может быть пустой строкой.',
            'null': 'Обязательное поле.'
        }
    )
    password = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        error_messages={
            'blank': 'Поле не может быть пустой строкой.',
            'null': 'Обязательное поле.'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
