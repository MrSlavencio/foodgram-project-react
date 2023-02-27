from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.utils.translation import gettext_lazy as _


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
    

    # USER = 'user'
    # MODERATOR = 'moderator'
    # ADMIN = 'admin'

    # ROLE_CHOICES = (
    #     (USER, 'Пользователь'),
    #     (MODERATOR, 'Модератор'),
    #     (ADMIN, 'Администратор'),
    # )

    # username = models.CharField(
    #     _('Имя пользователя'),
    #     max_length=150,
    #     unique=True,
    #     help_text=_(
    #         'Обязательное поле. 150 символов или меньше.'
    #         'Только буквы, цифры или символы @/./+/-/_.'
    #         'Не может быть <me>.'
    #     ),
    #     error_messages={
    #         'unique': _("Пользователь с таким именем уже существует"),
    #     },
    # )
    # email = models.EmailField(
    #     _('Адрес электронной почты'),
    #     unique=True,
    #     max_length=254,)
    # first_name = models.CharField(_('Имя'), max_length=150, blank=True)
    # last_name = models.CharField(_('Фамилия'), max_length=150, blank=True)
    # role = models.CharField(
    #     max_length=max(len(c) for c, _ in ROLE_CHOICES),
    #     choices=ROLE_CHOICES,
    #     default=USER,
    # )
    # bio = models.TextField(
    #     _('Биография'),
    #     blank=True,
    # )
    # confirmation_code = models.CharField(
    #     'Код подтверждения',
    #     max_length=255,
    #     blank=True,
    # )

    # REQUIRED_FIELDS = ["email", ]

    # class Meta:
    #     ordering = ("id", )
    #     verbose_name = _('Пользователь')
    #     verbose_name_plural = _('Пользователи')

    # def __str__(self):
    #     return self.username

    # @ property
    # def is_user(self):
    #     return self.role == self.USER

    # @ property
    # def is_admin(self):
    #     return self.role == self.ADMIN

    # @ property
    # def is_moderator(self):
    #     return self.role == self.MODERATOR
