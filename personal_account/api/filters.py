from django_filters import rest_framework as filters

from downtimes.models import Downtime


class DowntimeDatesFilter(filters.FilterSet):
    start_from = filters.DateFilter(
        method="start_from_filter"
    )
    start_to = filters.DateFilter(
        method="start_to_filter"
    )
    end_from = filters.DateFilter(
        method="end_from_filter"
    )
    end_to = filters.DateFilter(
        method="end_to_filter"
    )

    class Meta:
        model = Downtime
        fields = ("start_from", "start_to", "end_from", "end_to")

    def start_from_filter(self, queryset, name, value):
        return (
            queryset.filter(start_downtime__date__gte=value)
            if value else queryset
        )

    def start_to_filter(self, queryset, name, value):
        return (
            queryset.filter(start_downtime__date__lte=value)
            if value else queryset
        )

    def end_from_filter(self, queryset, name, value):
        return (
            queryset.filter(end_downtime__date__gte=value)
            if value else queryset
        )

    def end_to_filter(self, queryset, name, value):
        return (
            queryset.filter(end_downtime__date__lte=value)
            if value else queryset
        )
