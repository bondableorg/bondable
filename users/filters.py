from django_filters import rest_framework as filters

from .models import Home

# # We create filters for each field we want to be able to filter on
# class LocationFilter(filters.FilterSet):
#     name = filters.CharFilter(lookup_expr='icontains')
#     address = filters.CharFilter(lookup_expr='icontains')
#     year__gt = filters.NumberFilter(field_name='year', lookup_expr='gt')
#     year__lt = filters.NumberFilter(field_name='year', lookup_expr='lt')
#     creator__username = filters.CharFilter(lookup_expr='icontains')

#     class Meta:
#         model = Location
#         fields = ['title', 'genre', 'year', 'year__gt', 'year__lt', 'creator__username']
