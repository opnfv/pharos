from celery import shared_task
from datetime import timedelta
from django.utils import timezone

from jenkins.models import JenkinsStatistic
from notification.models import BookingNotification


@shared_task
def database_cleanup():
    now = timezone.now()
    JenkinsStatistic.objects.filter(timestamp__lt=now - timedelta(weeks=4)).delete()
    BookingNotification.objects.filter(submit_time__lt=now - timedelta(weeks=4)).delete()