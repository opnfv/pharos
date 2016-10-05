##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

from jenkins.models import JenkinsSlave


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(User, related_name='user_lab_owner', null=True)
    vpn_users = models.ManyToManyField(User, related_name='user_vpn_users', blank=True)
    slave = models.ForeignKey(JenkinsSlave, on_delete=models.DO_NOTHING, null=True)

    def get_booking_utilization(self, weeks):
        """
        Return a dictionary containing the count of booked and free seconds for a resource in the
        range [now,now + weeks] if weeks is positive,
        or [now-weeks, now] if weeks is negative
        """

        length = timedelta(weeks=abs(weeks))
        now = timezone.now()

        start = now
        end = now + length
        if weeks < 0:
            start = now - length
            end = now

        bookings = self.booking_set.filter(start__lt=start + length, end__gt=start)

        booked_seconds = 0
        for booking in bookings:
            booking_start = booking.start
            booking_end = booking.end
            if booking_start < start:
                booking_start = start
            if booking_end > end:
                booking_end = start + length
            total = booking_end - booking_start
            booked_seconds += total.total_seconds()

        return {'booked_seconds': booked_seconds,
                'available_seconds': length.total_seconds() - booked_seconds}

    class Meta:
        db_table = 'resource'

    def __str__(self):
        return self.name


class Server(models.Model):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    cpu = models.CharField(max_length=100, blank=True)
    ram = models.CharField(max_length=100, blank=True)
    storage = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'server'

    def __str__(self):
        return self.name
