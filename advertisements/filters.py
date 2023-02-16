from django_filters import rest_framework as filters, DateFromToRangeFilter

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['title', 'creator', 'created_at', 'status']


# Вместо использования filterset_fields для автоматического создания набора фильтров задайте его с помощью
# filterset_class (Docs) и используйте DateFromToRangeFilter [django-filter docs]
# для обеспечения фильтрации по диапазону дат:
# https://django.fun/ru/qa/10855/ - ссылка на статью

