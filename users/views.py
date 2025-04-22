import stripe
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from lms.models import Course
from .models import Payment, User, Subscription
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .services import (
    create_stripe_product,
    create_stripe_price,
    create_checkout_session,
)


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


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                {"message": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)


class CreatePaymentAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                {"message": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        amount = course.price  # Предполагается, что у модели Course есть поле price

        product = create_stripe_product(course)
        price = create_stripe_price(product, amount)
        session = create_checkout_session(
            price.id,
            success_url=f"http://localhost:8000/users/payments/success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"http://localhost:8000/users/payments/cancel/",
        )

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=amount,
            payment_method="stripe",
            stripe_session_id=session.id,
            stripe_payment_intent_id=session.payment_intent,
            stripe_checkout_url=session.url,
        )

        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckPaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response(
                {"message": "session_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)

            payment = Payment.objects.get(stripe_session_id=session_id)
            if payment_intent.status == "succeeded":
                payment.payment_status = "paid"
            elif payment_intent.status == "canceled":
                payment.payment_status = "failed"
            payment.save()

            return Response(
                {"status": payment_intent.status}, status=status.HTTP_200_OK
            )
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
