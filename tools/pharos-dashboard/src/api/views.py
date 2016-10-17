##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

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


@method_decorator(login_required, name='dispatch')
class GenerateTokenView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.delete()
            Token.objects.create(user=user)
        return redirect('account:settings')
