##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


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