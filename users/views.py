from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payment


from users.serializers import PaymentSerializer, UserSerializer

from rest_framework.permissions import AllowAny

from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserCreateAPIView(CreateAPIView):
    """UserCreateAPIView endpoint"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """UserListAPIView endpoint"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(UpdateAPIView):
    """UserUpdateAPIView endpoint"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDestroyAPIView(DestroyAPIView):
    """UserDestroyAPIView endpoint"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get('password'))
        user.save()


class PaymentAPIViewSet(ModelViewSet):
    """PaymentAPIViewSet endpoint"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('type_of_payment',)
    ordering_fields = ('date_of_payment',)


class PaymentCreateAPIView(CreateAPIView):
    """PaymentCreateAPIView endpoint"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        stripe_product_id = create_stripe_product(payment)
        price = create_stripe_price(stripe_product_id)
        payment_id, payment_link = create_stripe_session(price)
        payment.payment_id = payment_id
        payment.payment_link = payment_link
        payment.save()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """PaymentUpdateAPIView endpoint"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """PaymentDestroyAPIView endpoint"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
