import django_filters
from django_filters.rest_framework import FilterSet
from .models import Payment


class PaymentFilter(FilterSet):
    course = django_filters.NumberFilter(field_name="course", lookup_expr="exact")
    lesson = django_filters.NumberFilter(field_name="lesson", lookup_expr="exact")
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_method"]
