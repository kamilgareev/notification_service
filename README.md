
# Сервис уведомлений

Используемые технологии: Django, Django REST Framework, RabbitMQ, Celery, Flower

## Установка и запуск проекта
 - Клонирование репозитория
````
git clone https://github.com/kamilgareev/notification_service
````
- Создание виртуального окружения
````
python -m venv venv
````
- Активация виртуального окружения
````
venv\Scripts\activate
````
- Установка необходимых зависимостей 
````
pip install -r requirements.txt
````
- Установка параметров среды в файле .env
````
BASE_URL = '...'
SECRET_KEY = '...'
DEBUG_STATUS = ...
BASE_URL = '...'

#Параметры для взаимодейтсвия с внешним сервисом
MSG_SERVICE_URL = '...'
TOKEN = '...'

#Параметры базы данных
DB_ENGINE = '...'
DB_NAME = '...'
DB_USER = '...'
DB_PASSWORD = '...'
DB_HOST = '...'
DB_PORT = ...

#Параметры для отправки статистики по почте
EMAIL_USE_TLS = ...
EMAIL_HOST = '...'
EMAIL_HOST_USER = '...'
EMAIL_HOST_PASSWORD = '...'
EMAIL_PORT = ...
STATISTICS_RECIPIENTS = '...'
````
- Создание и применение миграций
```
python manage.py makemigrations
python manage.py migrate
```
- Запуск сервера RabbitMQ из встроенной командной строки
```
rabbitmq-server start
```
- Запуск Celery
```
celery -A notification_service worker -l info --pool=solo
```
- Запуск Flower
```
celery -A notification_service flower --loglevel=info
```
## URL проекта
- ### Flower
```
http://127.0.0.1:5555/
```

- ### API для модели Клиент

    - POST
    ```
    http://127.0.0.1:8000/clients/
    ```
    - PUT, PATCH, DELETE
    ```
    http://127.0.0.1:8000/clients/{id}/
    ```
- ### API для модели Рассылка

    - GET (информация о конкретной рассылке и обо всех рассылках)
    ```
    http://127.0.0.1:8000/distributions/{id}
    ```
    ```
    http://127.0.0.1:8000/distributions/
    ```
    - POST
    ```
    http://127.0.0.1:8000/distributions/
    ```
    - PUT, PATCH, DELETE
    ```
    http://127.0.0.1:8000/distributions/{id}
    ```
