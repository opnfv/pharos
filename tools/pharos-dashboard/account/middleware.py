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
