# rent_car

1. Создайте файл .env в корневом каталоге со следующими переменными:
```bash
DJANGO_SECRET_KEY=<Задайте ваш секртеный ключ>
DJANGO_DEBUG=False

DOMAIN_NAME=127.0.0.0

DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=<Задайте имя пользователя>
POSTGRES_PASSWORD=<Задайте пароль пользователя>
DJANGO_DATABASE_HOST=db
DJANGO_DATABASE_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=<Задайте хост e-mail для отправки e-mail>
EMAIL_HOST_USER=<Задайте e-mail пользователя для отправки e-mail>
EMAIL_HOST_PASSWORD=<Задайте пароль e-mail пользователя для отправки e-mail>

DJANGO_USERNAME_ADMIN=admin
DJANGO_PASSWORD_ADMIN=admin
DJANGO_EMAIL_ADMIN=admin@admin.com
```
2. Запустите комманду ```docker-compose up --build``` в корневом каталоге приложения.

В сервис аренды автомобиля будут загружены тестовые данные, 
чтобы можно было проверить функционал.