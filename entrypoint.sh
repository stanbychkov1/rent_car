#!/bin/sh
sleep 15
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py add_users
python manage.py add_cars
python manage.py add_rents
python manage.py initadmin

exec "$@"