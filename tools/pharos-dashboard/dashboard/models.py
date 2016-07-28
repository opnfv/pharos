from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    # Bookings should be deleted before resources
    resource = models.ForeignKey('Resource', models.PROTECT)
    # delete Booking when user is deleted
    user = models.ForeignKey(User, models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    creation = models.DateTimeField(auto_now=True)
    purpose = models.CharField(max_length=300)

    class Meta:
        db_table = 'booking'

    # check for conflicting bookings before saving
    def save(self, *args, **kwargs):
        # conflicts end after booking starts, and start before booking ends
        conflicting_bookings = Booking.objects.filter(resource_id=self.resource_id)
        conflicting_bookings = conflicting_bookings.filter(end_date_time__gt=self.start_date_time)
        conflicting_bookings = conflicting_bookings.filter(start_date_time__lt=self.end_date_time)
        # we may change a booking, so it is not a conflict
        conflicting_bookings = conflicting_bookings.exclude(booking_id=self.booking_id)
        if conflicting_bookings.count() > 0:
            raise ValueError('This booking overlaps with another booking')
        super(Booking, self).save(*args, **kwargs)


def __str__(self):
    return 'Booking: ' + str(self.resource)


class Pod(models.Model):
    pod_id = models.AutoField(primary_key=True)
    # Delete Pod with resource
    resource = models.ForeignKey('Resource', models.CASCADE)
    chassis = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'pod'

    def __str__(self):
        if self.chassis is None:
            return str(self.pod_id) + ' ' + str(self.resource)
        return str(self.pod_id) + ' ' + self.chassis


class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slavename = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    bookable = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'resource'

    def __str__(self):
        return self.name


class Server(models.Model):
    server_id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource, models.DO_NOTHING)
    model = models.CharField(max_length=200, blank=True, null=True)
    cpu = models.CharField(max_length=200, blank=True, null=True)
    ram = models.CharField(max_length=200, blank=True, null=True)
    storage = models.CharField(max_length=200, blank=True, null=True)
    count = models.IntegerField(default=1)

    class Meta:
        db_table = 'server'


class UserResource(models.Model):
    user_resource_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    # Delete if Resource is deleted
    resource = models.ForeignKey(Resource, models.CASCADE)

    class Meta:
        db_table = 'user_resource'
