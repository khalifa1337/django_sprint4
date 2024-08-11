from django.db import models


class PublishedModel(models.Model):
    """
    Абстрактная модель. Добвляет общее для моделей поле:
    is_published (обязательное) - для хранения информации о том, нужно ли
    выводить публикацию;
    created_at - для хранения информации о том, когда была добавлена запись
    """

    is_published = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class CreatedAtModel(models.Model):
    """
    Абстрактная модель. Добвляет общее для моделей поле:
    created_at - для хранения информации о том, когда была добавлена запись
    """

    created_at = models.DateTimeField(
        null=False,
        blank=False,
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
        ordering = ('-created_at',)
