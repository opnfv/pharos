##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from django.db import models
from django.utils import timezone


class JenkinsSlave(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=30, default='offline')
    url = models.CharField(max_length=1024)
    ci_slave = models.BooleanField(default=False)
    dev_pod = models.BooleanField(default=False)

    building = models.BooleanField(default=False)

    last_job_name = models.CharField(max_length=1024, default='')
    last_job_url = models.CharField(max_length=1024, default='')
    last_job_scenario = models.CharField(max_length=50, default='')
    last_job_branch = models.CharField(max_length=50, default='')
    last_job_installer = models.CharField(max_length=50, default='')
    last_job_result = models.CharField(max_length=30, default='')

    active = models.BooleanField(default=False)

    def get_utilization(self, timedelta):
        """
        Return a dictionary containing the count of idle, online and offline measurements in the time from
        now-timedelta to now
        """
        utilization = {'idle': 0, 'online': 0, 'offline': 0}
        statistics = self.jenkinsstatistic_set.filter(timestamp__gte=timezone.now() - timedelta)
        utilization['idle'] = statistics.filter(idle=True).count()
        utilization['online'] = statistics.filter(online=True).count()
        utilization['offline'] = statistics.filter(offline=True).count()
        return utilization

    class Meta:
        db_table = 'jenkins_slave'

    def __str__(self):
        return self.name


class JenkinsStatistic(models.Model):
    id = models.AutoField(primary_key=True)
    slave = models.ForeignKey(JenkinsSlave, on_delete=models.CASCADE)
    offline = models.BooleanField(default=False)
    idle = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jenkins_statistic'
