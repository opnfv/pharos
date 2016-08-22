from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    """
    Activate the timezone from request.user.userprofile if user is authenticated,
    deactivate the timezone otherwise and use default (UTC)
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            timezone.activate(request.user.userprofile.timezone)
        else:
            timezone.deactivate()
