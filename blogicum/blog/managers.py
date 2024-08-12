from django.db import models

from .querysets import PostQuerySet


class PublishedPostManager(models.Manager):
    """Менеджер для получения отфильтрованного QuerySet."""

    def get_queryset(self) -> models.QuerySet:
        return (
            PostQuerySet(self.model)
            .with_actual_data()
            .published()
            .category_published()
            .ordered_by_pub_date()
        )

    def with_comment_count(self):
        """Метод для получения числа комментариев для админ-панели"""
        return self.get_queryset().with_comment_count()
