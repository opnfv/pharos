from dashboard.models import Booking
import django.forms as forms
from django.utils.translation import ugettext_lazy as _


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date_time', 'end_date_time', 'purpose', 'booking_id']

        PURPOSE = {
            'id': 'purposefield',
            'type': 'text',
            'placeholder': 'Booking purpose',
        }

        widgets = {
            'purpose': forms.TextInput(attrs=PURPOSE),
        }

    # DATETIMEFORMAT should be equivalent to the moment.js format string that datetimepicker is
    # using ('YYYY-MM-DD HH:00 ZZ'). The string is used to create a timezone aware datetime object
    DATETIMEFORMAT = '%Y-%m-%d %H:%M %z'
    start_date_time = forms.DateTimeField(input_formats=[DATETIMEFORMAT, ], label='Start')
    end_date_time = forms.DateTimeField(input_formats=[DATETIMEFORMAT, ], label='End')

    # we need this to determine if we create a new booking or change an existing booking
    booking_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        if 'start_date_time' not in cleaned_data or 'end_date_time' not in cleaned_data:
            raise forms.ValidationError('Date Missing', code='missing_date')
        if cleaned_data['start_date_time'] >= cleaned_data['end_date_time']:
            raise forms.ValidationError(
                'Start date is after end date', code='invalid_dates')
        return cleaned_data
