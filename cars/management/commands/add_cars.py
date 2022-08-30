import csv
import os

from django.core.management import BaseCommand

from cars import models
from rent_car import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(settings.BASE_DIR, 'test_data/add_cars.csv'),
            encoding='utf-8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                car, created = models.Car.objects.get_or_create(
                    id=row[0],
                    title=row[1],
                    title_en=row[2],
                    prod_year=row[3],
                    owner_id=row[4])
                if created:
                    print(f'Car {car.title_en} created')
                else:
                    print(f'Car {car.title_en} already existed')
