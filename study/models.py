from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(
        upload_to="courses/photo", null=True, blank=True, verbose_name="Превью", help_text="Загрузите изображение")
    description = models.CharField(max_length=100, verbose_name="Описание")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Владелец',
                              help_text='Укажите владельца курса')
    video = models.CharField(
        max_length=100,
        null=True, blank=True,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )

    def __str__(self):
        return f"{self.name} {self.image} {self.description}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ("name",)


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название",
        help_text="Введите название урока",
    )
    description = models.CharField(
        max_length=100, verbose_name="Описание", help_text="Введите описание урока"
    )
    image = models.ImageField(
        upload_to="lessons/photo", null=True, blank=True, verbose_name="Превью", help_text="Загрузите изображение"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        null=True,
        blank=True,
        related_name="lessons",
    )
    video = models.CharField(
        max_length=100,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Владелец', help_text='Укажите владельца урока')

    def __str__(self):
        return (
            f"{self.name} {self.description} {self.image} {self.course} {self.video}")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ("name",)


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь',
                             on_delete=models.CASCADE, **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, **NULLABLE)
    is_sub = models.BooleanField(verbose_name="Подписка", default=False)

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
