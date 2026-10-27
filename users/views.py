from requests import Response
from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from educations.models import Course
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, SubscriptionsSerializer
from django_filters.rest_framework import DjangoFilterBackend


class UserAPICreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('payment_method', 'paid_course', 'paid_lesson')
    ordering_fields = ['pay_date']





