import csv
import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from rent_car import settings

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.all().count() != 0:
            return print('All users have already been created before')
        with open(
            os.path.join(settings.BASE_DIR, 'test_data/add_users.csv'),
            encoding='utf-8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                user = User.objects.create(
                    username=row[0],
                    email=row[1],
                    language=row[2],
                    first_name=row[3],
                    last_name=row[4],
                )
                user.set_password(row[5])
                user.save()
                print(f'User {user.email} created')
