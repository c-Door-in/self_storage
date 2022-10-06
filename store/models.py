from django.db import models
from django.contrib.auth.models import User


class Application(models.Model):
    email_adress = models.EmailField(default='Почта пользователя', verbose_name='Почта пользователя')

    def __str__(self):
        return self.email_adress


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(verbose_name='Фото пользователя')
    phone_number = models.CharField(null=True, blank=True, max_length=10, verbose_name='Телефон пользователя')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Storage(models.Model):
    location_city = models.CharField(default='Москва', max_length=35, verbose_name='Город')
    location_street_name = models.CharField(default='Тверская', max_length=35, verbose_name='Улица')
    location_street_number = models.CharField(default='15', max_length=10, verbose_name='Идентификатор дома')
    store_temperature = models.DecimalField(verbose_name='Температура на складе', decimal_places=2, max_digits=5)
    ceiling_height = models.DecimalField(verbose_name='Высота потолка', decimal_places=2, max_digits=5)
    payment_per_month = models.DecimalField(verbose_name='Оплата за месяц', decimal_places=2, max_digits=10)
    photo = models.ImageField(blank=True, verbose_name='Фото')
    note = models.CharField(null=True, blank=True, max_length=35, verbose_name='Заметка')
    total_boxes = models.IntegerField(null=True)


    def __str__(self):
        return self.location_city


class Box(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент', blank=True, null=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name='Склад')
    number = models.CharField(max_length=20, verbose_name='Номер в базе данных')
    is_use = models.BooleanField(default=False, verbose_name='Занятость бокса')
    rental_start_time = models.DateTimeField(null=True, verbose_name='Время начала аренды', blank=True)
    rental_end_time = models.DateTimeField(null=True, verbose_name='Время окончания аренды', blank=True)
    level = models.IntegerField(verbose_name='Этаж')
    square = models.IntegerField(verbose_name='Площадь', null=True)
    volume = models.CharField(verbose_name='Объём', max_length=15, null=True)
    price = models.DecimalField(verbose_name='Цена', decimal_places=4, max_digits=10)

    def __str__(self):
        return f'Бокс {self.number} склада {self.storage.location_city}'
