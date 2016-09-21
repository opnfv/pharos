##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from account.models import UserProfile


class AccountMiddlewareTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(username='user1')
        self.user1.set_password('user1')
        self.user1profile = UserProfile.objects.create(user=self.user1)
        self.user1.save()

    def test_timezone_middleware(self):
        """
        The timezone should be UTC for anonymous users, for authenticated users it should be set
        to user.userprofile.timezone
        """
        #default
        self.assertEqual(timezone.get_current_timezone_name(), 'UTC')

        url = reverse('account:settings')
        # anonymous request
        self.client.get(url)
        self.assertEqual(timezone.get_current_timezone_name(), 'UTC')

        # authenticated user with UTC timezone (userprofile default)
        self.client.login(username='user1', password='user1')
        self.client.get(url)
        self.assertEqual(timezone.get_current_timezone_name(), 'UTC')

        # authenticated user with custom timezone (userprofile default)
        self.user1profile.timezone = 'Etc/Greenwich'
        self.user1profile.save()
        self.client.get(url)
        self.assertEqual(timezone.get_current_timezone_name(), 'Etc/Greenwich')
