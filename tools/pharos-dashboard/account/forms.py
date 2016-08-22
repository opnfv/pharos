import django.forms as forms
import pytz as pytz

from registration.forms import RegistrationForm as BaseRegistrationForm


class AccountSettingsForm(forms.Form):
    fields = ['first_name', 'last_name', 'email', 'company', 'ssh_public_key', 'pgp_public_key',
              'timezone']

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    company = forms.CharField(max_length=30)
    ssh_public_key = forms.CharField(max_length=2048, widget=forms.Textarea)
    pgp_public_key = forms.CharField(max_length=2048, widget=forms.Textarea)
    timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones], initial='UTC')