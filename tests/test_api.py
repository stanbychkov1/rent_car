import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from cars import models

User = get_user_model()


class TestAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_signup_new_user(self, client):
        url = '/api/v1/signup/'
        data = {
            'first_name': 'stan',
            'email': 's@s.ru',
            'password': '1234',
            'username': 'stanley',
            'language': 'EN'
        }
        response = client.post(url, data=data)

        assert response.status_code == 201, \
            f'Регистрация пользователя недоступна'

    @pytest.mark.django_db(transaction=True)
    def test_02_get_token(self, client, admin):
        url = '/api/v1/token/'
        data = {
            'email': admin.email,
            'password': '1234567'
        }
        response = client.post(url, data=data)

        assert response.status_code == 200, \
            f'Получение токена невозможно'
        assert 'token' in response.data, \
            f'При передаче пары email, password сервер не выдает токен'

    @pytest.mark.django_db(transaction=True)
    def test_03_users_cars(self, client, user):
        url = '/api/v1/user_cars/'
        models.Car.objects.create(
            title='БМВ',
            title_en='BMW',
            prod_year=2000,
            owner_id=user.id
        )
        token, created = Token.objects.get_or_create(user=user)
        headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
        response = client.get(url, **headers)

        assert response.status_code == 200, \
            f'Проверьте, что {url} существует'
        assert len(response.data['results']) == 1, \
            f'Проверьте, что {url} выдает правильные данные'

        response = client.get(url)

        assert response.status_code == 401, \
            f'Проверьте, что пользователи без токена' \
            f' не могут получить доступ к {url}'

    @pytest.mark.django_db(transaction=True)
    def test_04_all_users(self, client, user):
        url = '/api/v1/all_users/'
        token, created = Token.objects.get_or_create(user=user)
        headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
        response = client.get(url, **headers)

        assert response.status_code == 200, \
            f'Проверьте, что {url} существует'
        assert len(response.data['results']) == 1, \
            f'Проверьте, что {url} выдает правильные данные'

        response = client.get(url)

        assert response.status_code == 401, \
            f'Проверьте, что пользователи без токена' \
            f' не могут получить доступ к {url}'

    @pytest.mark.django_db(transaction=True)
    def test_05_profile(self, client, user):
        url = '/api/v1/me/'
        token, created = Token.objects.get_or_create(user=user)
        headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
        response = client.get(url, **headers)

        assert response.status_code == 200, \
            f'Проверьте, что {url} существует'
        assert len(response.data) == 5, \
            f'Проверьте, что {url} выдает правильные данные'

        response = client.get(url)

        assert response.status_code == 401, \
            f'Проверьте, что пользователи без токена' \
            f' не могут получить доступ к {url}'

        data = {
            'first_name': 'stanley'
        }
        response = client.patch(url, data=data,
                                content_type='application/json', **headers)

        assert response.status_code == 200, \
            f'Проверьте, что {url} дает изменить данные пользователя'

        response = client.patch(url, data=data,
                                content_type='application/json')

        assert response.status_code == 401, \
            f'Проверьте, что пользователи без токена' \
            f' не могут получить доступ к {url}'
