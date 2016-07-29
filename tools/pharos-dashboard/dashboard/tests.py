import dashboard.jenkins.jenkins_adapter as jenkins
from django.test import SimpleTestCase


# Tests that the data we get with the jenkinsadapter contains all the
# data we need. These test will fail if;
# - there is no internet connection
# - the opnfv jenkins url has changed
# - the jenkins api has changed
# - jenkins is not set up / there is no data
class JenkinsAdapterTestCase(SimpleTestCase):
    def test_get_all_slaves(self):
        slaves = jenkins.get_all_slaves()
        self.assertTrue(len(slaves) > 0)
        for slave in slaves:
            self.assertTrue('displayName' in slave)
            self.assertTrue('idle' in slave)
            self.assertTrue('offline' in slave)

    def test_get_ci_slaves(self):
        slaves = jenkins.get_ci_slaves()
        self.assertTrue(len(slaves) > 0)
        for slave in slaves:
            self.assertTrue('nodeName' in slave)

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
