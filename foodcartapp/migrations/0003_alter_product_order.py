# Generated by Django 3.2 on 2022-05-18 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0002_alter_product_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='foodcartapp.order', verbose_name='Заказ'),
        ),
    ]