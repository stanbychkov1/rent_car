import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from dotenv import load_dotenv

load_dotenv()

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = os.getenv('DJANGO_EMAIL_ADMIN')
        if not User.objects.filter(email=email).exists():
            id = User.objects.latest('id').id + 1
            username = os.getenv('DJANGO_USERNAME_ADMIN')
            password = os.getenv('DJANGO_PASSWORD_ADMIN')
            User.objects.create_superuser(
                id=id,
                username=username,
                password=password,
                email=email,
            )
            print('Admin user initialized')
        else:
            print('Admin user has already been initialized')

