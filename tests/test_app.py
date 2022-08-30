import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from cars import models

User = get_user_model()


class TestAPP:
    data = {
        'first_name': 'stan',
        'email': 's@s.ru',
        'password1': '1234',
        'language': 'EN'
    }

    @pytest.mark.django_db(transaction=True)
    def test_01_signup_new_user(self, client):
        url = '/auth/signup/'
        response = client.get(url)

        assert response.status_code == 200, \
            f'Проверьте, что {url} существует'

        response = client.post(url, data=self.data)

        assert response.status_code in (301, 302), \
            f'Регистрация пользователя недоступна'
        assert User.objects.all().count() == 1, \
            f'Пользователь не создан'

    @pytest.mark.django_db(transaction=True)
    def test_02_login(self, client, admin):
        url = '/auth/login/'
        response = client.get(url)

        assert response.status_code == 200, \
            f'Проверьте, что {url} существует'

        response = client.post(url, data={
            'username': admin.email,
            'password': '1234567'
        })

        assert response.status_code in (301, 302), \
            f'Авторизация пользователя недоступна'
