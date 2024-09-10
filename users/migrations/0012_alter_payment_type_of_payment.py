# Generated by Django 4.2.15 on 2024-09-10 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_payment_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='type_of_payment',
            field=models.CharField(choices=[('cash', 'Наличные'), ('transfer', 'Перевод на счет')], verbose_name='Способ оплаты: наличные или перевод на счет.'),
        ),
    ]
