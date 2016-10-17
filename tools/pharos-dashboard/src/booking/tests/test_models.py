##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from datetime import timedelta

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.utils import timezone

from booking.models import *
from dashboard.models import Resource
from jenkins.models import JenkinsSlave


class BookingModelTestCase(TestCase):
    def setUp(self):
        self.slave = JenkinsSlave.objects.create(name='test', url='test')
        self.owner = User.objects.create(username='owner')

        self.res1 = Resource.objects.create(name='res1', slave=self.slave, description='x',
                                            url='x',owner=self.owner)
        self.res2 = Resource.objects.create(name='res2', slave=self.slave, description='x',
                                            url='x',owner=self.owner)

        self.user1 = User.objects.create(username='user1')

        self.add_booking_perm = Permission.objects.get(codename='add_booking')
        self.user1.user_permissions.add(self.add_booking_perm)

        self.user1 = User.objects.get(pk=self.user1.id)

        self.installer = Installer.objects.create(name='TestInstaller')
        self.scenario = Scenario.objects.create(name='TestScenario')

    def test_start_end(self):
        """
        if the start of a booking is greater or equal then the end, saving should raise a
        ValueException
        """
        start = timezone.now()
        end = start - timedelta(weeks=1)
        self.assertRaises(ValueError, Booking.objects.create, start=start, end=end,
                          resource=self.res1, user=self.user1)
        end = start
        self.assertRaises(ValueError, Booking.objects.create, start=start, end=end,
                          resource=self.res1, user=self.user1)

    def test_conflicts(self):
        """
        saving an overlapping booking on the same resource should raise a ValueException
        saving for different resources should succeed
        """
        start = timezone.now()
        end = start + timedelta(weeks=1)
        self.assertTrue(
            Booking.objects.create(start=start, end=end, user=self.user1, resource=self.res1))

        self.assertRaises(ValueError, Booking.objects.create, start=start,
                          end=end, resource=self.res1, user=self.user1)
        self.assertRaises(ValueError, Booking.objects.create, start=start + timedelta(days=1),
                          end=end - timedelta(days=1), resource=self.res1, user=self.user1)

        self.assertRaises(ValueError, Booking.objects.create, start=start - timedelta(days=1),
                          end=end, resource=self.res1, user=self.user1)
        self.assertRaises(ValueError, Booking.objects.create, start=start - timedelta(days=1),
                          end=end - timedelta(days=1), resource=self.res1, user=self.user1)

        self.assertRaises(ValueError, Booking.objects.create, start=start,
                          end=end + timedelta(days=1), resource=self.res1, user=self.user1)
        self.assertRaises(ValueError, Booking.objects.create, start=start + timedelta(days=1),
                          end=end + timedelta(days=1), resource=self.res1, user=self.user1)

        self.assertTrue(Booking.objects.create(start=start - timedelta(days=1), end=start,
                                               user=self.user1, resource=self.res1))
        self.assertTrue(Booking.objects.create(start=end, end=end + timedelta(days=1),
                                               user=self.user1, resource=self.res1))

        self.assertTrue(
            Booking.objects.create(start=start - timedelta(days=2), end=start - timedelta(days=1),
                                   user=self.user1, resource=self.res1))
        self.assertTrue(
            Booking.objects.create(start=end + timedelta(days=1), end=end + timedelta(days=2),
                                   user=self.user1, resource=self.res1))
        self.assertTrue(
            Booking.objects.create(start=start, end=end,
                                   user=self.user1, resource=self.res2, scenario=self.scenario,
                                   installer=self.installer))