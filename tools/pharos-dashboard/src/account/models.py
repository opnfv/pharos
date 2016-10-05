##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from django.db import models

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from dashboard.models import Resource

def upload_to(object, filename):
    return object.user.username + '/' + filename

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=100, blank=False, default='UTC')
    ssh_public_key = models.FileField(upload_to=upload_to, null=True, blank=True)
    pgp_public_key = models.FileField(upload_to=upload_to, null=True, blank=True)
    company = models.CharField(max_length=200, blank=False)

    oauth_token = models.CharField(max_length=1024, blank=False)
    oauth_secret = models.CharField(max_length=1024, blank=False)

    jira_url = models.CharField(max_length=100, default='')
    full_name = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return self.user.username
