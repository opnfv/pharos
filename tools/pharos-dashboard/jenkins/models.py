from django.db import models


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
