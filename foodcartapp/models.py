from tkinter import CASCADE
from tokenize import blank_re
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
from django.db.models import F, Sum
from django.utils import timezone
from collections import defaultdict


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )
    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):

    def get_amount_order(self):
        amount_order = self.annotate(
            amount=Sum(F('order_items__quantity') *
                       F('order_items__product__price'))
        )
        return amount_order


class Order(models.Model):
    ORDER_STATUS = (
        ('unprocessed', 'Необработанный'),
        ('processed', 'Обработанный'),
    )
    PAYMENT_METHOD = (
        ('cashless', 'Безналичный'),
        ('cash', 'Наличные'),
    )
    address = models.CharField(
        'Адрес',
        max_length=150,
        db_index=True,
    )
    commentary = models.TextField('Комментарий', blank=True)
    firstname = models.CharField(
        'Имя',
        max_length=50,
        db_index=True,
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=50,
        db_index=True,
    )
    phonenumber = PhoneNumberField(
        'Телефон',
        region='RU',
        db_index=True,
    )
    order_status = models.CharField(
        'Статус',
        max_length=12,
        choices=ORDER_STATUS,
        default='unprocessed',
        db_index=True,
    )
    registrated_at = models.DateTimeField(
        'Дата регистрации',
        default=timezone.now,
        db_index=True,
    )
    called_at = models.DateTimeField(
        'Дата звонка',
        blank=True,
        null=True,
        db_index=True,
    )
    delivered_at = models.DateTimeField(
        'Дата доставки',
        blank=True,
        null=True,
        db_index=True,
    )
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=12,
        blank=True,
        choices=PAYMENT_METHOD,
        db_index=True,
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Ресторан',
        related_name='restorans',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.firstname


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='order_items',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        related_name='product_items',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField('Количество')
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Пункт заказа'
        verbose_name_plural = 'Пункты заказа'

    def __str__(self):
        return f'{self.product.name} {self.order.firstname} {self.order.address}'
