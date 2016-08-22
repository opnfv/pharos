from django.db import models

from django.contrib.auth.models import User

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

    class Meta:
        db_table = 'user_profile'
