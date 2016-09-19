from rest_framework import serializers

from booking.models import Booking
from dashboard.models import Server, Resource


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'resource', 'start', 'end', 'purpose')


class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Server
        fields = ('id', 'resource', 'name', 'model', 'cpu', 'ram', 'storage')


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'description', 'url', 'server_set')
