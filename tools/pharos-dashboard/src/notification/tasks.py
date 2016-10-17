##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from notification.models import BookingNotification
from notification_framework.notification import Notification


@shared_task
def send_booking_notifications():
    messaging = Notification(dashboard_url=settings.RABBITMQ_URL)

    now = timezone.now()
    notifications = BookingNotification.objects.filter(submitted=False,
                                                       submit_time__gt=now,
                                                       submit_time__lt=now + timedelta(minutes=5))
    for notification in notifications:
        messaging.send(notification.type, notification.booking.resource.name,
                       notification.get_content())
        notification.submitted = True
        notification.save()
