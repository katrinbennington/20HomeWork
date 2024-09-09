# Generated by Django 4.2.15 on 2024-09-09 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study', '0008_subscription_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='course',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='status',
        ),
        migrations.AddField(
            model_name='subscription',
            name='course_subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='study.course', verbose_name='курс в подписке'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='is_sub',
            field=models.BooleanField(default=False, verbose_name='подписка'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
