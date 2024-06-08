from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, verbose_name='логин')
    email = models.EmailField(verbose_name='почта', **NULLABLE)
    time_left = models.IntegerField(default=100, verbose_name='оставшееся время')
    tg_name = models.CharField(max_length=40, verbose_name='ник в ТГ', **NULLABLE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
