import django_filters

from . import models


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = models.Product
        fields = {
            'gender': ['exact'],
            'category': ['exact'],
            'brand': ['exact'],
        }
