from django.db.models.signals import post_save
from django.dispatch import receiver
from notification_service.settings import TIME_ZONE
from .models import Distribution
from .tasks import distribution_process, send_statistics
from datetime import datetime
import pytz
from notification_service.settings import STATISTICS_RECIPIENTS


@receiver(post_save, sender=Distribution)
def start_distribution(sender, instance, created, **kwargs):
    send_statistics.apply_async(
        args=[STATISTICS_RECIPIENTS]
    )
    if instance.start_date_time < datetime.now(tz=pytz.timezone(TIME_ZONE)) < instance.end_date_time:
        distribution_process.apply_async(
            args=[instance.id],
            expires=instance.end_date_time
        )
    if datetime.now(tz=pytz.timezone(TIME_ZONE)) < instance.start_date_time:
        distribution_process.apply_async(
            args=[instance.id],
            expires=instance.end_date_time,
            eta=instance.start_date_time
        )
