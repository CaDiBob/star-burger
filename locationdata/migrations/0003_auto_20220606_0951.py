# Generated by Django 3.2 on 2022-06-06 09:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('locationdata', '0002_alter_location_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Адрес')),
                ('lat', models.FloatField(db_index=True, verbose_name='Широта')),
                ('lon', models.FloatField(db_index=True, verbose_name='Долгота')),
                ('created_at', models.DateField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Местоположение ресторана',
                'verbose_name_plural': 'Местоположения ресторанов',
            },
        ),
        migrations.RenameModel(
            old_name='Location',
            new_name='OrderLocation',
        ),
        migrations.AlterModelOptions(
            name='orderlocation',
            options={'verbose_name': 'Местоположение зказа', 'verbose_name_plural': 'Местоположения заказов'},
        ),
    ]
