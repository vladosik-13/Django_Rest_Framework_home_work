from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PaymentListView, UserCreateAPIView, SubscriptionAPIView

app_name = "users"

urlpatterns = [
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("subscribe/", SubscriptionAPIView.as_view(), name="subscribe"),
]
