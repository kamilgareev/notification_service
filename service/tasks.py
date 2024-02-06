import pytz
from celery.utils.log import get_task_logger
from django.core.mail import get_connection, EmailMessage
from notification_service import settings
from .models import Client, Distribution, Message
from notification_service.celery import app
from notification_service.settings import TIME_ZONE
from datetime import datetime
import requests
from notification_service.settings import MSG_SERVICE_URL, TOKEN, BASE_URL

logger = get_task_logger(__name__)

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


@app.task(bind=True, retry_backoff=True)
def send_message(self, url, data):
    try:
        requests.post(url=url,
                      headers=headers,
                      json=data)
        message = Message.objects.get(id=data['id'])
        message.distribution_status = 'Y'
        logger.info(f'Message {data["id"]} is successfully sent')
    except requests.exceptions.RequestException as exc:
        logger.error(f'Error with message {data["id"]}. Details: {exc}')
        raise self.retry(exc=exc, max_retries=10)


@app.task(bind=True, retry_backoff=True)
def distribution_process(self, distribution_id):
    distribution = Distribution.objects.get(id=distribution_id)
    messages = Message.objects.filter(distribution__id=distribution_id)
    clients = distribution.filter_clients()
    for message in messages:
        url = MSG_SERVICE_URL + str(message.id)
        client = message.client
        data = {
            "id": message.id,
            "phone": int(str(client.phone_number)),
            "text": distribution.text,
        }
        if message.distribution_time < datetime.now(tz=pytz.timezone(TIME_ZONE)):
            send_message.apply_async(
                args=[url, data],
                eta=message.distribution_time
            )
        else:
            send_message.apply_async(
                args=[url, data]
            )


@app.task(bind=True)
def send_statistics(self, recipient_list):
    with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = 'Distribution statistics'
        email_from = settings.EMAIL_HOST_USER
        data = requests.get(url=BASE_URL+'/distributions/').text
        data = data.split()

        message = f'Statistics:\n {data}'
        sent = EmailMessage(subject, message, email_from, recipient_list,
                            connection=connection).send()
    time_delta = 60 * 60 * 24
    send_statistics.apply_async(args=[recipient_list], countdown=time_delta)
