from requests import Response, session
from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from users.models import Payment, User, Pay
from users.serializers import PaymentSerializer, UserSerializer, PaySerializer
from django_filters.rest_framework import DjangoFilterBackend

from users.services import create_stripe_price, create_stripe_session


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


class PayAPICreateView(CreateAPIView):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.amount)
        session_id, link_on_pay = create_stripe_session(price)
        payment.session_id = session_id
        payment.link_on_pay = link_on_pay
        payment.save()



