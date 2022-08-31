import pytest
import datetime
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from cars import models

from users import forms


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

    @pytest.mark.django_db(transaction=True)
    def test_03_index_not_auth(self, client):
        url = '/'
        response = client.get(url)

        assert response.status_code == 302, \
            f'Проверьте, что неавторизованный пользователь не может получить' \
            f'доступ к {url}'

    @pytest.mark.django_db(transaction=True)
    def test_04_index(self, user_client):
        url = '/'

        response = user_client.get(url)

        assert response.status_code == 200, \
            f'Проверьте, что авторизованный пользователь может получить' \
            f'доступ к {url}'

    @pytest.mark.django_db(transaction=True)
    def test_05_rent_not_auth(self, client):
        url = '/rent/'
        response = client.get(url)

        assert response.status_code == 302, \
            f'Проверьте, что неавторизованный пользователь не может получить' \
            f'доступ к {url}'

    @pytest.mark.django_db(transaction=True)
    def test_06_rent(self, user_client, user, admin):
        start_date = datetime.date.today()
        end_date = datetime.date.today()+datetime.timedelta(days=1)
        url = f'/rent/?start_date={start_date}' \
              f'&end_date={end_date}'
        cars = models.Car.objects.bulk_create([
            models.Car(title='BMW', prod_year='1990', owner_id=user.id),
            models.Car(title='Mercedes', prod_year='1990', owner_id=admin.id)
        ])
        response = user_client.get(url)

        assert response.status_code == 200, \
            f'Проверьте, что можно получить доступ к автомобилям'

        assert len(response.context_data['object_list']) == 2, \
            f'Проверьте, что сервис выдает правильные данные'

        models.RentalPeriod.objects.create(
            car_id=cars[0].id, driver_id=user.id,
            start_date=start_date, end_date=end_date
        )

        response = user_client.get(url)

        assert len(response.context_data['object_list']) == 1, \
            f'Проверьте, что сервис выдает правильные данные'

        data = {
            'car': 2,
            'driver': admin.id,
            'start_date': start_date.__str__(),
            'end_date': end_date.__str__()
        }
        new_response = user_client.post(url, data=data)

        assert new_response.status_code in (301, 302), \
            f'Проверьте, что можно арендовать автомобиль'

    @pytest.mark.django_db(transaction=True)
    def test_07_profile_not_auth(self, client):
        url = '/auth/profile/'
        response = client.get(url)

        assert response.status_code == 302, \
            f'Проверьте, что неавторизованный пользователь не может получить' \
            f'доступ к {url}'

        url = '/auth/profile/update/'
        response = client.get(url)

        assert response.status_code == 302, \
            f'Проверьте, что неавторизованный пользователь не может получить' \
            f'доступ к {url}'

    @pytest.mark.django_db(transaction=True)
    def test_08_profile(self, user_client, user):
        url = '/auth/profile/'
        response = user_client.get(url)

        assert response.status_code == 200, \
            f'Проверьте, что можно получить доступ к данным профиля'
        assert response.context_data['form'].__class__ is forms.UserForm, \
            f'Проверьте, что отображаются правильные данные'

        url = '/auth/profile/update/?'
        response = user_client.get(url)

        assert response.status_code == 200, \
            f'Проверьте, что можно получить доступ к данным профиля'

        data = {
            'first_name': 'stanley',
            'last_name': 'stanley',
            'email': user.email,
            'language': 'EN',
            'username': 'stanley'
        }
        response = user_client.post(url, data=data)

        assert response.status_code in (301, 302), \
            f'Проверьте, что сервис дает изменить данные пользователя'
        user.refresh_from_db()
        assert user.first_name == 'stanley', \
            f'Проверьте, что сервис дает изменить данные пользователя'


