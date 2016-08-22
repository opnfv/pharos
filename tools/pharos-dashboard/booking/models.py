from django.contrib.auth.models import User
from django.db import models

from dashboard.models import Resource


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)  # delete if user is deleted
    resource = models.ForeignKey(Resource, models.PROTECT)
    start = models.DateTimeField()
    end = models.DateTimeField()

    purpose = models.CharField(max_length=300, blank=False)

    class Meta:
        db_table = 'booking'

    def authorization_test(self):
        """
        Return True if self.user is authorized to make this booking.
        """
        user = self.user
        # Check if User is troubleshooter / admin
        if user.has_perm('booking.add_booking'):
            return True
        # Check if User owns this resource
        if user in self.resource.owners.all():
            return True
        return False


    def save(self, *args, **kwargs):
        """
        Save the booking if self.user is authorized and there is no overlapping booking.
        Raise PermissionError if the user is not authorized
        Raise ValueError if there is an overlapping booking
        """
        if not self.authorization_test():
            raise PermissionError('Insufficient permissions to save this booking.')
        if self.start >= self.end:
            raise ValueError('Start date is after end date')
        # conflicts end after booking starts, and start before booking ends
        conflicting_dates = Booking.objects.filter(resource=self.resource)
        conflicting_dates = conflicting_dates.filter(end__gt=self.start)
        conflicting_dates = conflicting_dates.filter(start__lt=self.end)
        if conflicting_dates.count() > 0:
            raise ValueError('This booking overlaps with another booking')
        return super(Booking, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.resource) + ' from ' + str(self.start) + ' until ' + str(self.end)
