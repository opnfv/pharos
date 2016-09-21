from django.conf import settings
from django.contrib import admin

from notification.models import BookingNotification

if settings.DEBUG:
    admin.site.register(BookingNotification)