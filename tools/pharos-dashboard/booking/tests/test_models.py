from datetime import timedelta

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.utils import timezone

from booking.models import Booking
from dashboard.models import Resource


class BookingModelTestCase(TestCase):
    def setUp(self):
        self.res1 = Resource.objects.create(name='res1', slavename='s1', description='x', url='x')
        self.res2 = Resource.objects.create(name='res2', slavename='s2', description='x', url='x')

        self.user1 = User.objects.create(username='user1')

        self.add_booking_perm = Permission.objects.get(codename='add_booking')
        self.user1.user_permissions.add(self.add_booking_perm)

        self.user1 = User.objects.get(pk=self.user1.id)

    def test_start__end(self):
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
                                   user=self.user1, resource=self.res2))

    def test_authorization(self):
        user = User.objects.create(username='user')
        self.assertRaises(PermissionError, Booking.objects.create, start=timezone.now(),
                          end=timezone.now() + timedelta(days=1), resource=self.res1, user=user)
        self.res1.owners.add(user)
        self.assertTrue(
            Booking.objects.create(start=timezone.now(), end=timezone.now() + timedelta(days=1),
                                   resource=self.res1, user=user))
        user.user_permissions.add(self.add_booking_perm)
        user = User.objects.get(pk=user.id)
        self.assertTrue(
            Booking.objects.create(start=timezone.now(), end=timezone.now() + timedelta(days=1),
                                   resource=self.res2, user=user))
