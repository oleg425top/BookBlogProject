from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    image = models.ImageField(upload_to='users/images', blank=True, null=True, verbose_name='аватар')
    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(max_length=150, verbose_name='Имя', default='Аноним')
    is_active = models.BooleanField(default=True, verbose_name='active')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

