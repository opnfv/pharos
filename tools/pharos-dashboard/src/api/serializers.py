##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from rest_framework import serializers

from booking.models import Booking
from dashboard.models import Server, Resource, ResourceStatus


class BookingSerializer(serializers.ModelSerializer):
    installer_name = serializers.RelatedField(source='installer', read_only=True)
    scenario_name = serializers.RelatedField(source='scenario', read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'resource_id', 'start', 'end', 'installer_name', 'scenario_name', 'purpose')


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('id', 'resource_id', 'name', 'model', 'cpu', 'ram', 'storage')


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'description', 'url', 'server_set')

class ResourceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceStatus
        fields = ('id', 'resource', 'timestamp','type', 'title', 'content')