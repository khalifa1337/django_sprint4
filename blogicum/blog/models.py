from django.contrib.auth import get_user_model
from django.db import models

from core.constants import STANDART_MAX_LENGHT
from core.models import PublishedAndCreateModel
from django.urls import reverse


from .managers import PublishedPostManager
from .querysets import PostQuerySet

User = get_user_model()


class Category(PublishedAndCreateModel):
    """
    Модель для хранения данных о категориях.
    Содержит поля:
        title (обязательное) - заголовок категории
        description (обязательное) - описание категории
        slug (обязательное, уникальное) - идентификатор (слаг) категории
        is_published (обязательное) - доступость категории
        created_at (обязательное) - дата и время добавления категории
    """

    title = models.CharField(
        max_length=STANDART_MAX_LENGHT,
        null=False,
        blank=False,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta(PublishedAndCreateModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedAndCreateModel):
    """
    Модель для хранения данных о местоположениях.
    Содержит поля:
        name (обязательное) - название локации
        is_published (обязательное) - доступность локации
        created_at (обязательное) - дата и время создания
    """

    name = models.CharField(
        max_length=STANDART_MAX_LENGHT,
        null=False,
        blank=False,
        verbose_name='Название места'
    )

    class Meta(PublishedAndCreateModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedAndCreateModel):
    """
    Модель для хранения данных о постах.
    Содержит поля:
        title (обязательное) - заголовок поста
        text (обязательное) - содержимое поста
        pub_date (обязательное) - дата и время добавления поста
        author (обязательное) - ключ, автор поста
        location - ключ, местоположение
        category - ключ, категория поста
        is_published - доступность поста
        created_at - дата и время создания поста
    """

    title = models.CharField(
        max_length=STANDART_MAX_LENGHT,
        null=False,
        blank=False,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем '
            '— можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='posts',
        verbose_name='Категория'
    )
    image = models.ImageField(
        blank=True,
        upload_to='posts_images',
        verbose_name='Фото'
    )
    objects = PostQuerySet.as_manager()
    published = PublishedPostManager()

    class Meta(PublishedAndCreateModel.Meta):
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('created_at',)

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('blog:profile', kwargs={'username': self.author})

    def __str__(self):
        return self.title


class Comment(PublishedAndCreateModel):
    text = models.TextField('Текст комментария')
    comment_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)