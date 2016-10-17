##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from django.test import TestCase
from django.urls import reverse

from dashboard.models import Resource
from jenkins.models import JenkinsSlave


class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.slave_active = JenkinsSlave.objects.create(name='slave_active', url='x', active=True)
        self.slave_inactive = JenkinsSlave.objects.create(name='slave_inactive', url='x',
                                                          active=False)
        self.res_active = Resource.objects.create(name='res_active', slave=self.slave_active,
                                                  description='x', url='x')
        self.res_inactive = Resource.objects.create(name='res_inactive', slave=self.slave_inactive,
                                                    description='x', url='x')

    def test_booking_utilization_json(self):
        url = reverse('dashboard:booking_utilization', kwargs={'resource_id': 0, 'weeks': 0})
        self.assertEqual(self.client.get(url).status_code, 404)

        url = reverse('dashboard:booking_utilization', kwargs={'resource_id': self.res_active.id,
                                                               'weeks': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data')

    def test_jenkins_utilization_json(self):
        url = reverse('dashboard:jenkins_utilization', kwargs={'resource_id': 0, 'weeks': 0})
        self.assertEqual(self.client.get(url).status_code, 404)

        url = reverse('dashboard:jenkins_utilization', kwargs={'resource_id': self.res_active.id,
                                                               'weeks': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data')

    def test_jenkins_slaves_view(self):
        url = reverse('dashboard:jenkins_slaves')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.slave_active, response.context['slaves'])
        self.assertNotIn(self.slave_inactive, response.context['slaves'])

    def test_ci_pods_view(self):
        url = reverse('dashboard:ci_pods')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['ci_pods']), 0)

        self.slave_active.ci_slave = True
        self.slave_inactive.ci_slave = True
        self.slave_active.save()
        self.slave_inactive.save()

        response = self.client.get(url)
        self.assertIn(self.res_active, response.context['ci_pods'])
        self.assertNotIn(self.res_inactive, response.context['ci_pods'])

    def test_dev_pods_view(self):
        url = reverse('dashboard:dev_pods')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['dev_pods']), 0)

