import random
import string
import secrets

from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from users.forms import UserRegisterForm
from users.models import User, Payment

#from config.settings import EMAIL_HOST_USER
from django.views.generic import ListView

from users.serializers import PaymentSerializer, MyTokenObtainPairSerializer, UserSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentAPIViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('type_of_payment', 'payed_course_or_lesson')
    ordering_fields = ('date_of_payment',)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


# class PaymentUpdateAPIView(generics.UpdateAPIView):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
#
#
# class PaymentDestroyAPIView(generics.DestroyAPIView):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
