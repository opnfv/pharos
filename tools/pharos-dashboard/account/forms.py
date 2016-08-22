import django.forms as forms
import pytz as pytz

from account.models import UserProfile


class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['company', 'ssh_public_key', 'pgp_public_key', 'timezone']

    timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones], initial='UTC')
