##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import os
import sys
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from notification.models import BookingNotification

# this adds the top level directory to the python path, this is needed so that we can access the
# notification library
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from dashboard_notification.notification import Notification, Message


@shared_task
def send_booking_notifications():
    with Notification(dashboard_url=settings.RABBITMQ_URL, user=settings.RABBITMQ_USER, password=settings.RABBITMQ_PASSWORD) as messaging:
        now = timezone.now()
        notifications = BookingNotification.objects.filter(submitted=False,
                                                           submit_time__gt=now - timedelta(minutes=1),
                                                           submit_time__lt=now + timedelta(minutes=5))
        for notification in notifications:
            message = Message(type=notification.type, topic=notification.booking.resource.name,
                              content=notification.get_content())
            messaging.send(message)
            notification.submitted = True
            notification.save()

@shared_task
def notification_debug():
    with Notification(dashboard_url=settings.RABBITMQ_URL) as messaging:
        notifications = BookingNotification.objects.all()
        for notification in notifications:
            message = Message(type=notification.type, topic=notification.booking.resource.name,
                              content=notification.get_content())
            messaging.send(message)
