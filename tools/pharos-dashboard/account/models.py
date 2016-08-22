from django.db import models

from django.contrib.auth.models import User

from dashboard.models import Resource


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=100, blank=False, default='UTC')
    ssh_public_key = models.CharField(max_length=2048, blank=False)
    pgp_public_key = models.CharField(max_length=2048, blank=False)
    company = models.CharField(max_length=200, blank=False)
    oauth_token = models.CharField(max_length=1024, blank=False)
    oauth_secret = models.CharField(max_length=1024, blank=False)

    class Meta:
        db_table = 'user_profile'
