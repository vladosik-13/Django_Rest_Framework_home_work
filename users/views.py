from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny

from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter
from rest_framework.filters import OrderingFilter


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
    filter_backends = [OrderingFilter]
    ordering_fields = ["payment_date"]  # Разрешаем сортировку по дате оплаты
    ordering = ["-payment_date"]  # По умолчанию сортируем по убыванию даты оплаты


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data["password"])
        user.save()
