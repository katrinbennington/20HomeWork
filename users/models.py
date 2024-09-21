from django.contrib.auth.models import AbstractUser
from django.db import models

from study.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email address")
    phone_number = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE, help_text="Введите номер телефона")
    country = models.CharField(max_length=100, verbose_name="Страна", **NULLABLE)
    avatar = models.ImageField(upload_to="users/photo", verbose_name="Аватар", help_text="Загрузите свой аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    payment_type = (
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date_of_payment = models.DateTimeField(verbose_name='Дата оплаты')
    payed_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    payed_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cумма оплаты')
    type_of_payment = models.CharField(choices=payment_type, verbose_name="Способ оплаты: наличные или перевод на счет.")
    payment_link = models.URLField(max_length=400, verbose_name='Cсылка на оплату', blank=True, null=True)
    payment_id = models.CharField(max_length=255, verbose_name='Id платежа', blank=True, null=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return str(self.payment_amount)
