from django.urls import reverse

from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models
from taggit.managers import TaggableManager


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=50, verbose_name='название')
    slug = models.SlugField(max_length=50, unique_for_date='publish', verbose_name='слаг')
    body = models.TextField(verbose_name='содержание')
    publish = models.DateTimeField(default=timezone.now, verbose_name='дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлен')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='статус')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='автор')

    objects = models.Manager()
    published = PublishManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                            self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug
                        ])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='к посту')
    name = models.CharField(max_length=80, verbose_name='Заголовок коммента')
    email = models.EmailField(verbose_name='почта')
    body = models.TextField(verbose_name='содержание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлен')
    active = models.BooleanField(default=True, verbose_name='активность')

    class Meta:
        ordering = ['created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        indexes = [
            models.Index(fields=['created']),
        ]


    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

