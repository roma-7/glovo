import django_filters
from .models import *


class ProductListFilter(django_filters.FilterSet):
    price_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
        }


class ProductComboListFilter(django_filters.FilterSet):
    price_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = ProductCombo
        fields = {
            'category': ['exact'],
        }
