from django.db import models
from phone_field import PhoneField
from pytz import all_timezones
from notification_service.settings import TIME_ZONE


class Client(models.Model):
    timezones = tuple(zip(all_timezones, all_timezones))
    phone_number = PhoneField(null=False,
                              blank=False,
                              unique=True,
                              verbose_name='Client phone number',
                              max_length=11)
    phone_code = models.CharField(max_length=3,
                                  blank=True,
                                  verbose_name='Client code')
    tag = models.CharField(max_length=50,
                           blank=True,
                           verbose_name='Client tag')
    timezone = models.CharField(max_length=32,
                                choices=timezones,
                                default=TIME_ZONE,
                                verbose_name='Client time zone')

    def __str__(self):
        return f'Client {self.id}, phone number: {self.phone_number}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Distribution(models.Model):
    text = models.TextField(blank=False,
                            verbose_name='Message text')
    start_date_time = models.DateTimeField(null=False,
                                           blank=False,
                                           verbose_name='Distribution start time and date')
    end_date_time = models.DateTimeField(null=False,
                                         blank=False,
                                         verbose_name='Distribution end time and date')
    client_code = models.CharField(blank=False,
                                   max_length=3,
                                   verbose_name='Distribution client code')
    client_tag = models.CharField(blank=False,
                                  max_length=3,
                                  verbose_name='Distribution client tag')

    def filter_clients(self):
        return Client.objects.filter(phone_code=self.client_code, tag=self.client_tag)

    def __str__(self):
        return f'Distribution {self.id}, {self.start_date_time}-{self.end_date_time}'

    class Meta:
        verbose_name = 'Distribution'
        verbose_name_plural = 'Distributions'


class Message(models.Model):
    status_choices = (
        ('Y', 'Yes'),
        ('N', 'No')
    )
    distribution_time = models.DateTimeField(null=False,
                                             blank=False,
                                             verbose_name='Message distribution time and date')
    distribution_status = models.CharField(max_length=1,
                                           choices=status_choices,
                                           verbose_name='Message distribution status')
    client = models.ForeignKey(Client,
                               related_name='Client',
                               on_delete=models.CASCADE)
    distribution = models.ForeignKey(Distribution,
                                     related_name='Distribution',
                                     on_delete=models.CASCADE)

    def __str__(self):
        return f'Message {self.id}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
