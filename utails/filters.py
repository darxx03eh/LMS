import django_filters
from django.db.models import Avg
from django_filters import FilterSet

from api.models import Course


class CourseFilter(FilterSet):
    instructor = django_filters.CharFilter(field_name="instructor__username")
    rate__gte = django_filters.NumberFilter(method="filter_by_rate")
    rate__lte = django_filters.NumberFilter(method="filter_by_rate")

    def filter_by_rate(self, queryset, name, value):
        queryset = queryset.annotate(avg_rate=Avg("course_feedbacks__rate"))
        if name == "rate__gte":
            return queryset.filter(avg_rate__gte=value)
        elif name == "rate__lte":
            return queryset.filter(avg_rate__lte=value)
        return queryset

    class Meta:
        model = Course
        fields = {"category": ["iexact", "icontains"], "instructor": ["exact"]}
