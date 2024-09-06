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

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

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
    payment_item = (
        ("course", "Курс"),
        ("lesson", "Урок"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date_of_payment = models.DateTimeField(verbose_name='Дата оплаты')
    payed_course_or_lesson = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', blank=True,
                                     null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    type_of_payment = models.CharField(choices=payment_type, verbose_name="Способ оплаты: наличные или перевод на счет.")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.email
