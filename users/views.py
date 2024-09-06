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
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from users.forms import UserRegisterForm
from users.models import User, Payment

#from config.settings import EMAIL_HOST_USER
from django.views.generic import ListView

from users.serializers import PaymentSerializer


class UserListView(LoginRequiredMixin, ListView):
    model = User

class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class PasswordResetView(View):
    form_class = PasswordResetForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'users/reset_password.html', {'form': form})

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            user.password = make_password(new_password)
            user.save()
            send_mail(
                subject='Восстановление пароля',
                message=f'Здравствуйте, вы запрашивали обновление пароля. Ваш новый пароль: {new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return render(request, 'users/password_reset_done.html')
        except User.DoesNotExist:
            return render(request, 'users/reset_password.html', {'error': 'Пользователь с таким email не найден.'})


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
