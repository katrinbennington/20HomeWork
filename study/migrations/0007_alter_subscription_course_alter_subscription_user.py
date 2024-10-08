# Generated by Django 4.2.15 on 2024-09-09 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study', '0006_alter_lesson_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscription_course', to='study.course', verbose_name='Курс'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
