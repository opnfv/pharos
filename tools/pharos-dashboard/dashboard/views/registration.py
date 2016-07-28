from django.contrib.auth.mixins import UserPassesTestMixin


class BookingUserTestMixin(UserPassesTestMixin):
    # Test if a user has permission to book this Pod
    def test_func(self):
        user = self.request.user
        # Check if User is troubleshooter / admin
        if user.has_perm(('dashboard.add_booking')):
            return True
        # Check if User owns this resource
        user_resources = user.userresource_set.get_queryset()
        for user_resource in user_resources:
            if user_resource.resource_id == self.resource.resource_id:
                return True
        return False
