from django_filters import rest_framework as filters
from stuffs.models import Unit

class UnitFilter(filters.FilterSet):
    serial = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Unit
        fields = ['serial']