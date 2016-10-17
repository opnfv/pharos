##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from datetime import timedelta
from unittest import TestCase

from django.contrib.auth.models import User
from django.utils import timezone

from booking.models import Booking
from dashboard.models import Resource
from jenkins.models import JenkinsSlave
from notification.models import *


class JenkinsModelTestCase(TestCase):
    def setUp(self):
        self.slave = JenkinsSlave.objects.create(name='test1', url='test')
        self.res1 = Resource.objects.create(name='res1', slave=self.slave, description='x',
                                            url='x')
        self.user1 = User.objects.create(username='user1')

        start = timezone.now()
        end = start + timedelta(days=1)
        self.booking = Booking.objects.create(start=start, end=end, purpose='test',
                                              resource=self.res1, user=self.user1)

    def test_booking_notification(self):
        BookingNotification.objects.create(type='test', booking=self.booking,
                                           submit_time=timezone.now())

        self.assertRaises(ValueError, BookingNotification.objects.create, type='test',
                          booking=self.booking,
                          submit_time=timezone.now())
