from celery import shared_task
from datetime import timedelta

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
