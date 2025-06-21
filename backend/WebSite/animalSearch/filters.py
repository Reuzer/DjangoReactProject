import django_filters
from django.db import models
from .models import Pet_Report

class PetReportFilter(django_filters.FilterSet):
    report_type = django_filters.CharFilter(field_name='report_type')
    pet_type = django_filters.NumberFilter(field_name='breed_id__pet_type_id')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Pet_Report
        fields = ['report_type', 'pet_type']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(special_marks__icontains=value) |
            models.Q(location__icontains=value)
        )