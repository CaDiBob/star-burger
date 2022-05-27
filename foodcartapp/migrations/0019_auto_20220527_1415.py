# Generated by Django 3.2 on 2022-05-27 14:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0018_order_commentary'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='called_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата звонка'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='registrated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации'),
        ),
    ]
