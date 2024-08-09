from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    """Отдельная фильтрация QurySet для постов"""

    def with_actual_data(self):
        """Фильтрация актуальной даты."""
        return self.filter(pub_date__lte=timezone.now())

    def published(self):
        """Фильтрация доступности для публикации."""
        return self.filter(is_published=True)

    def category_published(self):
        """Фильтрация доступности категории."""
        return self.filter(category__is_published=True)

    def ordered_by_pub_date(self):
        """Сортировка постов по дате публикации (по убыванию)."""
        return self.order_by('-pub_date')
