from django_filters import rest_framework as filters
from stuffs.models import Unit

class UnitFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    barcode = filters.CharFilter(lookup_expr='icontains')
    date_purchased = filters.DateFilter(lookup_expr='iexact')

    class Meta:
        model = Unit
        fields = ['name', 'category', 'date_purchased']