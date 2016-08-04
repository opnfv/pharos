from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from registration.backends.simple.views import RegistrationView

from dashboard.forms.account_settings_form import AccountSettingsForm
from dashboard.models import UserProfile


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


class DashboardRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return "/accounts/settings"


@method_decorator(login_required, name='dispatch')
class AccountSettingsView(FormView):
    form_class = AccountSettingsForm
    template_name = 'registration/account_settings.html'
    success_url = '/'

    def get_initial(self):
        user = self.request.user
        try:
            user.userprofile
        except ObjectDoesNotExist:
            UserProfile.objects.create(user=user)
            messages.add_message(self.request, messages.INFO,
                                 'Please complete your user profile')
        initial = super(AccountSettingsView, self).get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        initial['company'] = user.userprofile.company
        initial['ssh_public_key'] = user.userprofile.sshkey
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.userprofile.company = form.cleaned_data['company']
        user.userprofile.sshkey = form.cleaned_data['ssh_public_key']
        user.userprofile.save()
        user.save()
        return super(AccountSettingsView,self).form_valid(form)
