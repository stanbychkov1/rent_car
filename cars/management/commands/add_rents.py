import csv
import os

from django.core.management import BaseCommand

from cars import models
from rent_car import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        if models.RentalPeriod.objects.all().count() != 0:
            return 'All rents have already been created before'
        with open(
            os.path.join(settings.BASE_DIR, 'test_data/add_rents.csv'),
            encoding='utf-8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rental_period = models.RentalPeriod.objects.create(
                    car_id=row[0],
                    driver_id=row[1],
                    start_date=row[2],
                    end_date=row[3])
                print(f'Rent {rental_period.id} created')
