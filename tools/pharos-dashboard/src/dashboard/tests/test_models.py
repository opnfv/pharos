##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from datetime import timedelta
from math import ceil, floor

from django.test import TestCase
from django.utils import timezone

from booking.models import *
from dashboard.models import Resource
from jenkins.models import JenkinsSlave


class ResourceModelTestCase(TestCase):
    def setUp(self):
        self.slave = JenkinsSlave.objects.create(name='test', url='test')
        self.owner = User.objects.create(username='owner')

        self.res1 = Resource.objects.create(name='res1', slave=self.slave, description='x',
                                            url='x', owner=self.owner)

    def test_booking_utilization(self):
        utilization = self.res1.get_booking_utilization(1)
        self.assertTrue(utilization['booked_seconds'] == 0)
        self.assertTrue(utilization['available_seconds'] == timedelta(weeks=1).total_seconds())

        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(days=1)
        booking = Booking.objects.create(start=start, end=end, purpose='test', resource=self.res1,
                               user=self.owner)

        utilization = self.res1.get_booking_utilization(1)
        booked_seconds = timedelta(days=1).total_seconds()
        self.assertEqual(utilization['booked_seconds'], booked_seconds)

        utilization = self.res1.get_booking_utilization(-1)
        self.assertEqual(utilization['booked_seconds'], 0)

        booking.delete()
        start = timezone.now() - timedelta(days=1)
        end = start + timedelta(days=2)
        booking = Booking.objects.create(start=start, end=end, purpose='test', resource=self.res1,
                               user=self.owner)
        booked_seconds = self.res1.get_booking_utilization(1)['booked_seconds']
        # use ceil because a fraction of the booked time has already passed now
        booked_seconds = ceil(booked_seconds)
        self.assertEqual(booked_seconds, timedelta(days=1).total_seconds())

        booking.delete()
        start = timezone.now() + timedelta(days=6)
        end = start + timedelta(days=2)
        booking = Booking.objects.create(start=start, end=end, purpose='test', resource=self.res1,
                               user=self.owner)
        booked_seconds = self.res1.get_booking_utilization(1)['booked_seconds']
        booked_seconds = floor(booked_seconds)
        self.assertEqual(booked_seconds, timedelta(days=1).total_seconds())





