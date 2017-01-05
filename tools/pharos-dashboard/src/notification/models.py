##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from django.db import models

class BookingNotification(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    booking = models.ForeignKey('booking.Booking', on_delete=models.CASCADE)
    submit_time = models.DateTimeField()
    submitted = models.BooleanField(default=False)

    def get_content(self):
        return {
            'resource_id': self.booking.resource.id,
            'booking_id': self.booking.id,
            'user': self.booking.user.username,
            'user_id': self.booking.user.id,
        }

    def save(self, *args, **kwargs):
        notifications = self.booking.bookingnotification_set.filter(type=self.type).exclude(
            id=self.id)
        #if notifications.count() > 0:
        #    raise ValueError('Doubled Notification')
        return super(BookingNotification, self).save(*args, **kwargs)
