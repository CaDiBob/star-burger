# Generated by Django 3.2 on 2022-05-27 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0017_alter_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='commentary',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
    ]
