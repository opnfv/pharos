from rest_framework import viewsets

from api.serializers import ResourceSerializer, ServerSerializer, BookingSerializer
from booking.models import Booking
from dashboard.models import Resource, Server


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_fields = ('resource', 'user')


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filter_fields = ('resource', 'name')


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_fields = ('name',)