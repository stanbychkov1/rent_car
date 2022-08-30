import csv
import os

from django.core.management import BaseCommand

from cars import models
from rent_car import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        if models.Car.objects.all().count() != 0:
            return 'All cars have already been created before'
        with open(
            os.path.join(settings.BASE_DIR, 'test_data/add_cars.csv'),
            encoding='utf-8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                car = models.Car.objects.create(
                    title=row[0],
                    title_en=row[1],
                    prod_year=row[2],
                    owner_id=row[3])
                print(f'Car {car.title_en} created')
