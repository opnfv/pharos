##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from account.models import UserProfile


class TimezoneMiddleware(MiddlewareMixin):
    """
    Activate the timezone from request.user.userprofile if user is authenticated,
    deactivate the timezone otherwise and use default (UTC)
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                tz = request.user.userprofile.timezone
                timezone.activate(tz)
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=request.user)
                tz = request.user.userprofile.timezone
                timezone.activate(tz)
        else:
            timezone.deactivate()
