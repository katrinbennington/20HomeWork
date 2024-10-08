# Generated by Django 4.2.15 on 2024-09-21 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0012_alter_subscription_course_alter_subscription_is_sub_and_more'),
        ('users', '0015_payment_payment_id_payment_payment_link_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payed_course_or_lesson',
            new_name='payed_course',
        ),
        migrations.AddField(
            model_name='payment',
            name='payed_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='study.lesson', verbose_name='Оплаченный урок'),
        ),
    ]
