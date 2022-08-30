import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_superuser(
        username='TestUser',
        email='admin@fake.fake',
        password='1234567')


@pytest.fixture
def user():
    user = User.objects.create_user(
        username='TestUser1',
        email='testuser@fake.fake',
        password='12345',
    )
    return user


@pytest.fixture
def user_api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client
