from django.contrib.auth.models import User
from django.db import models


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slavename = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    owners = models.ManyToManyField(User)

    class Meta:
        db_table = 'resource'

    def __str__(self):
        return self.name

class ResourceUtilization(models.Model):
    POD_STATUS = {
        'online': 1,
        'idle': 2,
        'offline': 3
    }

    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_created=True)
    pod_status = models.IntegerField()