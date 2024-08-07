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
        )
