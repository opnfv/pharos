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

import jenkins.adapter as jenkins
from jenkins.models import *


# Tests that the data we get with the jenkinsadapter contains all the
# data we need. These test will fail if;
# - there is no internet connection
# - the opnfv jenkins url has changed
# - the jenkins api has changed
# - jenkins is not set up / there is no data
class JenkinsAdapterTestCase(TestCase):
    def test_get_all_slaves(self):
        slaves = jenkins.get_all_slaves()
        self.assertTrue(len(slaves) > 0)
        for slave in slaves:
            self.assertTrue('displayName' in slave)
            self.assertTrue('idle' in slave)
            self.assertTrue('offline' in slave)

    def test_get_slave(self):
        slaves = jenkins.get_all_slaves()
        self.assertEqual(slaves[0], jenkins.get_slave(slaves[0]['displayName']))
        self.assertEqual({}, jenkins.get_slave('098f6bcd4621d373cade4e832627b4f6'))

    def test_get_ci_slaves(self):
        slaves = jenkins.get_ci_slaves()
        self.assertTrue(len(slaves) > 0)
        for slave in slaves:
            self.assertTrue('nodeName' in slave)

    def test_get_jenkins_job(self):
        slaves = jenkins.get_ci_slaves()
        job = None
        for slave in slaves:
            job = jenkins.get_jenkins_job(slave['nodeName'])
            if job is not None:
                break
        # We need to test at least one job
        self.assertNotEqual(job, None)

    def test_get_all_jobs(self):
        jobs = jenkins.get_all_jobs()
        lastBuild = False
        self.assertTrue(len(jobs) > 0)
        for job in jobs:
            self.assertTrue('displayName' in job)
            self.assertTrue('url' in job)
            self.assertTrue('lastBuild' in job)
            if job['lastBuild'] is not None:
                lastBuild = True
                self.assertTrue('building' in job['lastBuild'])
                self.assertTrue('fullDisplayName' in job['lastBuild'])
                self.assertTrue('result' in job['lastBuild'])
                self.assertTrue('timestamp' in job['lastBuild'])
                self.assertTrue('builtOn' in job['lastBuild'])
        self.assertTrue(lastBuild)

    def test_parse_job(self):
        job = {
            "displayName": "apex-deploy-baremetal-os-nosdn-fdio-noha-colorado",
            "url": "https://build.opnfv.org/ci/job/apex-deploy-baremetal-os-nosdn-fdio-noha-colorado/",
            "lastBuild": {
                "building": False,
                "fullDisplayName": "apex-deploy-baremetal-os-nosdn-fdio-noha-colorado #37",
                "result": "SUCCESS",
                "timestamp": 1476283629917,
                "builtOn": "lf-pod1"
            }
        }

        job = jenkins.parse_job(job)
        self.assertEqual(job['scenario'], 'os-nosdn-fdio-noha')
        self.assertEqual(job['installer'], 'apex')
        self.assertEqual(job['branch'], 'colorado')
        self.assertEqual(job['result'], 'SUCCESS')
        self.assertEqual(job['building'], False)
        self.assertEqual(job['url'],
                         "https://build.opnfv.org/ci/job/apex-deploy-baremetal-os-nosdn-fdio-noha-colorado/")
        self.assertEqual(job['name'],
                         'apex-deploy-baremetal-os-nosdn-fdio-noha-colorado')

    def test_get_slave_status(self):
        slave = {
            'offline': True,
            'idle': False
        }
        self.assertEqual(jenkins.get_slave_status(slave), 'offline')
        slave = {
            'offline': False,
            'idle': False
        }
        self.assertEqual(jenkins.get_slave_status(slave), 'online')
        slave = {
            'offline': False,
            'idle': True
        }
        self.assertEqual(jenkins.get_slave_status(slave), 'online / idle')


class JenkinsModelTestCase(TestCase):
    def test_get_utilization(self):
        jenkins_slave = JenkinsSlave.objects.create(name='test', status='offline', url='')
        utilization = jenkins_slave.get_utilization(timedelta(weeks=1))
        self.assertEqual(utilization['idle'], 0)
        self.assertEqual(utilization['offline'], 0)
        self.assertEqual(utilization['online'], 0)

        for i in range(10):
            JenkinsStatistic.objects.create(slave=jenkins_slave,
                                            offline=True, idle=True,
                                            online=True)

        utilization = jenkins_slave.get_utilization(timedelta(weeks=1))
        self.assertEqual(utilization['idle'], 10)
        self.assertEqual(utilization['offline'], 10)
        self.assertEqual(utilization['online'], 10)
