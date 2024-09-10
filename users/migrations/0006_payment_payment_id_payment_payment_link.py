# Generated by Django 4.2.15 on 2024-09-10 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Id платежа'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_link',
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name='Cсылка на оплату'),
        ),
    ]
