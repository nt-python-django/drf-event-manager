import django_filters

from .models import Event

class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    start_date = django_filters.DateTimeFilter(field_name="start_date", lookup_expr='gte')

    class Meta:
        model = Event
        fields = ['title', 'start_date']