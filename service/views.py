from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Client, Distribution, Message
from .serializers import ClientSerializer, DistributionSerializer, MessageSerializer
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse


class ClientViewSet(ViewSet):

    @swagger_auto_schema(
        operation_description='Create a new client',
        request_body=ClientSerializer,
        responses={201: ClientSerializer()}
    )
    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Update client data',
        request_body=ClientSerializer,
        responses={200: ClientSerializer()}
    )
    def update(self, request, pk=None):
        try:
            instance = Client.objects.filter(id=pk)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClientSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Update client data partially',
        request_body=ClientSerializer,
        responses={200: ClientSerializer()}
    )
    def partial_update(self, request, pk=None):
        try:
            instance = Client.objects.filter(id=pk)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClientSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Delete client data'
    )
    def destroy(self, request, pk=None):
        try:
            instance = Client.objects.filter(id=pk)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_200_OK)


class DistributionViewSet(ViewSet):

    @swagger_auto_schema(
        operation_description='All distributions info',
    )
    def list(self, request):
        all_distributions = Distribution.objects.all()
        finished_distributions = all_distributions.filter(end_date_time__lt=timezone.now())
        not_finished_distributions = all_distributions.filter(end_date_time__gt=timezone.now())
        finished_distributions_info = []
        for dist in finished_distributions:
            messages = Message.objects.filter(distribution__id=dist.id)
            sent_messages = messages.filter(distribution_status='Y')
            not_sent_messages = messages.filter(distribution_status='N')
            finished_distributions_info.append(
                {
                    'distribution_id': dist.id,
                    'info': {
                        'sent_messages_count': sent_messages.count(),
                        'not_sent_messages_count': not_sent_messages.count()
                    }
                }
            )
        content = {
            'finished_distributions_count': finished_distributions.count(),
            'finished_distributions_info': finished_distributions_info,
            'not_finished_distributions_count': not_finished_distributions.count(),
            'not_finished_distributions_info': list(not_finished_distributions.values())
        }
        return JsonResponse(content)

    @swagger_auto_schema(
        operation_description='Distribution info',
    )
    def retrieve(self, request, pk=None):
        try:
            messages = Message.objects.filter(distribution__id=pk)
        except Distribution.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        sent_messages = messages.filter(distribution_status='Y')
        not_sent_messages = messages.filter(distribution_status='N')
        content = {'distribution_id': pk,
                   'sent_messages_count': sent_messages.count(),
                   'sent_messages:': list(sent_messages.values()),
                   'not_sent_messages_count': not_sent_messages.count(),
                   'not_sent_messages': list(not_sent_messages.values())
                   }
        return JsonResponse(content)

    @swagger_auto_schema(
        operation_description='Create a new distribution',
        request_body=DistributionSerializer,
        responses={201: DistributionSerializer()}
    )
    def create(self, request):
        serializer = DistributionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Update distribution data',
        request_body=DistributionSerializer,
        responses={200: DistributionSerializer()}
    )
    def update(self, request, pk=None):
        try:
            instance = Distribution.objects.filter(id=pk)
        except Distribution.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DistributionSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Update distribution data partially',
        request_body=ClientSerializer,
        responses={200: ClientSerializer()}
    )
    def partial_update(self, request, pk=None):
        try:
            instance = Distribution.objects.filter(id=pk)
        except Distribution.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DistributionSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Delete distribution data'
    )
    def destroy(self, request, pk=None):
        try:
            instance = Distribution.objects.filter(id=pk)
        except Distribution.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_200_OK)
