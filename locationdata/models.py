from django.db import models
from django.utils import timezone


class Location(models.Model):
    address = models.CharField('Адрес', max_length=100, db_index=True, unique=True)
    lat = models.FloatField('Широта', db_index=True)
    lon = models.FloatField('Долгота', db_index=True)
    created_at = models.DateField('Дата', default=timezone.now, db_index=True)

    class Meta:
        verbose_name = 'Местоположение зказа'
        verbose_name_plural = 'Местоположения заказов'

    def __str__(self):
        return self.address
