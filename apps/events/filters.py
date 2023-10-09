import django_filters

from .models import Event


class EventFilter(django_filters.FilterSet):
    registration_end_date = django_filters.DateFilter(
        field_name='registration_end_date',
        lookup_expr='gte'
    )
    participants_quantity = django_filters.NumberFilter(
        field_name='participants_quantity',
        lookup_expr='gte'
    )

    class Meta:
        model = Event
        fields = ['registration_end_date', 'participants_quantity']
