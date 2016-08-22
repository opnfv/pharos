from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from jenkins.models import JenkinsSlave


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    owners = models.ManyToManyField(User)
    slave = models.ForeignKey(JenkinsSlave, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'resource'

    def __str__(self):
        return self.name