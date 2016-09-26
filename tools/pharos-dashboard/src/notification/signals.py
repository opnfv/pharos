##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from django.db.models.signals import post_save
from django.dispatch import receiver

from booking.models import Booking
from notification.models import BookingNotification


@receiver(post_save, sender=Booking)
def booking_notification_handler(sender, instance, **kwargs):
    BookingNotification.objects.update_or_create(
        booking=instance, type='booking_start', defaults={'submit_time': instance.start}
    )
    BookingNotification.objects.update_or_create(
        booking=instance, type='booking_end', defaults={'submit_time': instance.end}
    )