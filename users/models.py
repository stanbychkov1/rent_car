from django.contrib.auth.models import AbstractUser
from django.db import models

LANGUAGES = (
    ('EN', 'en'),
    ('RU', 'ru')
)


class MyUser(AbstractUser):
    username = models.CharField(max_length=50, unique=False, null=True,
                                blank=True, verbose_name='Ник')
    language = models.CharField(max_length=255,
                                choices=LANGUAGES,
                                blank=False,
                                null=False,
                                verbose_name='Язык')
    email = models.EmailField(unique=True,
                              verbose_name='E-mail')
    first_name = models.CharField(max_length=150, blank=True,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True,
                                 verbose_name='Фамилия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name
