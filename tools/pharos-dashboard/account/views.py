from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from registration.backends.simple.views import RegistrationView as BaseRegistrationView

from account.forms import AccountSettingsForm
from account.models import UserProfile


class RegistrationView(BaseRegistrationView):
    template_name = 'registration/registration_form.html'

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context.update({'title': "Registration"})
        return context

    def register(self, form):
        new_user = super(RegistrationView, self).register(form)
        UserProfile.objects.create(user=new_user)
        messages.add_message(self.request, messages.INFO, 'Please complete your user profile.')
        return new_user

    def get_success_url(self, user):
        return reverse('account:settings')


@method_decorator(login_required, name='dispatch')
class AccountSettingsView(FormView):
    form_class = AccountSettingsForm
    template_name = 'registration/registration_form.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        try:
            request.user.userprofile
        except ObjectDoesNotExist:
            UserProfile.objects.create(user=request.user)
            messages.add_message(self.request, messages.INFO,
                                 'Please complete your user profile to proceed.')
        return super(AccountSettingsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AccountSettingsView, self).get_context_data(**kwargs)
        context.update({'title': "Settings"})
        return context

    def get_initial(self):
        user = self.request.user
        initial = super(AccountSettingsView, self).get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        initial['company'] = user.userprofile.company
        initial['ssh_public_key'] = user.userprofile.sshkey
        initial['pgp_public_key'] = user.userprofile.pgpkey
        initial['timezone'] = user.userprofile.timezone
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.userprofile.company = form.cleaned_data['company']
        user.userprofile.sshkey = form.cleaned_data['ssh_public_key']
        user.userprofile.pgpkey = form.cleaned_data['pgp_public_key']
        user.userprofile.timezone = form.cleaned_data['timezone']
        user.userprofile.save()
        if not user.is_active:
            user.is_active = True
        user.save()
        messages.add_message(self.request, messages.INFO,
                             'Settings saved')
        return super(AccountSettingsView, self).form_valid(form)
