import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date=DateFilter(field_name="date_created",lookup_expr='gte')#apply filter on field='date_created  of Order modelgte-> greater than or equal to
    end_date=DateFilter(field_name="date_created", lookup_expr='lte')
    note=CharFilter(field_name="note", lookup_expr='icontains')#apply filter on note field , icontains-> if any query contains any part of search query than retutn it, 'i' in 'icontains' is to ignorer case-sensitive
    class Meta:
        model=Order #model on which you want to apply filter
        fields="__all__" #list of fields on which you want to apply filter (__all__ => include all attributes)
        exclude= ['customer', 'date_created'] #remove the filter for them
