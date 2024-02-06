from django.contrib import admin
from .models import Client, Distribution, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'tag', 'timezone']


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ['start_date_time', 'end_date_time', 'client_code', 'client_tag']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['distribution_time', 'distribution_status', 'client', 'distribution']

