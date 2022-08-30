import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

YEARS = [
    (year, year) for year in range(1990, datetime.date.today().year+1)
]


class Car(models.Model):
    title = models.CharField(max_length=255,
                             blank=False, verbose_name='Название')
    title_en = models.CharField(max_length=255,
                                blank=True, null=True,
                                verbose_name='Название на английском')
    prod_year = models.IntegerField(choices=YEARS,
                                    verbose_name='Год производства')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Создано')
    owner = models.ForeignKey(to=User,
                              on_delete=models.CASCADE,
                              related_name='car',
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f'Автомобиль {self.title}({self.title_en}) {self.prod_year}' \
               f' года производства.'


class RentalPeriod(models.Model):
    car = models.ForeignKey(to=Car,
                            on_delete=models.CASCADE,
                            related_name='rental_period',
                            verbose_name='Автомобиль')
    driver = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='rental_period',
                               verbose_name='Водитель')
    start_date = models.DateField(blank=False, null=False,
                                  verbose_name='Дата начала аренды')
    end_date = models.DateField(blank=False, null=False,
                                verbose_name='Дата конца аренды')

    class Meta:
        verbose_name = 'Период аренды'
        verbose_name_plural = 'Периоды аренды'

    def __str__(self):
        return f'Период аренды автомобиля {self.car.title} пользователя' \
               f' {self.driver} с {self.start_date}г. по {self.end_date}г.'

    @property
    def upcoming(self):
        if self.start_date > datetime.date.today():
            return True
        return False

    @property
    def current(self):
        if self.start_date <= datetime.date.today() <= self.end_date:
            return True
        return False

    @property
    def closed(self):
        if datetime.date.today() > self.end_date:
            return True
        return False
