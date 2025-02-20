from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter
from rest_framework.filters import OrderingFilter

class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
    filter_backends = [OrderingFilter]
    ordering_fields = ['payment_date']  # Разрешаем сортировку по дате оплаты
    ordering = ['-payment_date']  # По умолчанию сортируем по убыванию даты оплаты