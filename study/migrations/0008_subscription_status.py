# Generated by Django 4.2.15 on 2024-09-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0007_alter_subscription_course_alter_subscription_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='status',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='статус подписки'),
        ),
    ]
