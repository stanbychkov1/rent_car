import csv
import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from rent_car import settings

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(settings.BASE_DIR, 'test_data/add_users.csv'),
            encoding='utf-8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                user, created = User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    language=row[3],
                    first_name=row[4],
                    last_name=row[5],
                    password=row[6])
                if created:
                    print(f'User {user.email} created')
                else:
                    print(f'User {user.email} already existed')

