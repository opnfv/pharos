##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from datetime import timedelta

from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_text
from registration.forms import User

from account.models import UserProfile
from booking.models import Booking
from dashboard.models import Resource
from jenkins.models import JenkinsSlave


class BookingViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.slave = JenkinsSlave.objects.create(name='test', url='test')
        self.owner = User.objects.create(username='owner')
        self.res1 = Resource.objects.create(name='res1', slave=self.slave, description='x',
                                            url='x',owner=self.owner)
        self.user1 = User.objects.create(username='user1')
        self.user1.set_password('user1')
        self.user1profile = UserProfile.objects.create(user=self.user1)
        self.user1.save()

        self.user1 = User.objects.get(pk=self.user1.id)


    def test_resource_bookings_json(self):
        url = reverse('booking:bookings_json', kwargs={'resource_id': 0})
        self.assertEqual(self.client.get(url).status_code, 404)

        url = reverse('booking:bookings_json', kwargs={'resource_id': self.res1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content), {"bookings": []})
        booking1 = Booking.objects.create(start=timezone.now(),
                                          end=timezone.now() + timedelta(weeks=1), user=self.user1,
                                          resource=self.res1)
        response = self.client.get(url)
        json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('bookings', json)
        self.assertEqual(len(json['bookings']), 1)
        self.assertIn('start', json['bookings'][0])
        self.assertIn('end', json['bookings'][0])
        self.assertIn('id', json['bookings'][0])
        self.assertIn('purpose', json['bookings'][0])

    def test_booking_form_view(self):
        url = reverse('booking:create', kwargs={'resource_id': 0})
        self.assertEqual(self.client.get(url).status_code, 404)

        # authenticated user
        url = reverse('booking:create', kwargs={'resource_id': self.res1.id})
        self.client.login(username='user1',password='user1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('booking/booking_calendar.html')
        self.assertTemplateUsed('booking/booking_form.html')
        self.assertIn('resource', response.context)


    def test_booking_view(self):
        start = timezone.now()
        end = start + timedelta(weeks=1)
        booking = Booking.objects.create(start=start, end=end, user=self.user1, resource=self.res1)

        url = reverse('booking:detail', kwargs={'booking_id':0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse('booking:detail', kwargs={'booking_id':booking.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('booking/booking_detail.html')
        self.assertIn('booking', response.context)

    def test_booking_list_view(self):
        start = timezone.now() - timedelta(weeks=2)
        end = start + timedelta(weeks=1)
        Booking.objects.create(start=start, end=end, user=self.user1, resource=self.res1)

        url = reverse('booking:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('booking/booking_list.html')
        self.assertTrue(len(response.context['bookings']) == 0)

        start = timezone.now()
        end = start + timedelta(weeks=1)
        Booking.objects.create(start=start, end=end, user=self.user1, resource=self.res1)
        response = self.client.get(url)
        self.assertTrue(len(response.context['bookings']) == 1)