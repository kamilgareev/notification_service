from rest_framework.serializers import ModelSerializer
from .models import Client, Distribution, Message


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DistributionSerializer(ModelSerializer):
    class Meta:
        model = Distribution
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


