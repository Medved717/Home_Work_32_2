from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .apps import UsersConfig
from .views import (PaymentListAPIView, UserAPICreateView)

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserAPICreateView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('payments/list/', PaymentListAPIView.as_view(), name='payments_list'),
]


