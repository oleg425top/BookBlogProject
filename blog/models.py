from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=50, verbose_name='название')
    slug = models.SlugField(max_length=50, verbose_name='слаг')
    body = models.TextField(verbose_name='содержание')
    publish = models.DateTimeField(default=timezone.now, verbose_name='дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлен')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='статус')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='автор')

    objects = models.Manager()
    publish = models.PublishManager()

    class Meta:
        ordering = ['-publish']
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
