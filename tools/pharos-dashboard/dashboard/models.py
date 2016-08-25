from django.contrib.auth.models import User
from django.db import models

from jenkins.models import JenkinsSlave


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(User)
    slave = models.ForeignKey(JenkinsSlave, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'resource'

    def __str__(self):
        return self.name


class Server(models.Model):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    cpu = models.CharField(max_length=100, blank=True)
    ram = models.CharField(max_length=100, blank=True)
    storage = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'server'

    def __str__(self):
        return self.name
