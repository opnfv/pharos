import django.forms as forms


class BookingForm(forms.Form):
    fields = ['start_date_time', 'end_date_time', 'purpose', 'repeat',
              'repeat_interval', 'repeat_end']

    # DATETIMEFORMAT should be equivalent to the moment.js format string that datetimepicker is
    # using ('YYYY-MM-DD HH:00 ZZ'). The string is used to create a timezone aware datetime object
    DATETIMEFORMAT = '%Y-%m-%d %H:%M %z'
    start_date_time = forms.DateTimeField(input_formats=[DATETIMEFORMAT, ], label='Start')
    end_date_time = forms.DateTimeField(input_formats=[DATETIMEFORMAT, ], label='End')

    purpose = forms.CharField(max_length=300)

    repeat = forms.BooleanField(required=False)
    repeat_interval = forms.ChoiceField(choices=(('1', 'Daily'), ('2', 'Weekly'), ('3', 'Monthly')),
                                        required=False)
    repeat_end = forms.DateTimeField(input_formats=[DATETIMEFORMAT, ], label='Repeat until',
                                     required=False)

    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        if 'start_date_time' not in cleaned_data or 'end_date_time' not in cleaned_data:
            raise forms.ValidationError('Date Missing', code='missing_date')
        if cleaned_data['start_date_time'] >= cleaned_data['end_date_time']:
            raise forms.ValidationError(
                'Start date is after end date', code='invalid_dates')
        if cleaned_data['repeat']:
            if cleaned_data['repeat_interval'] is None or cleaned_data['repeat_end'] is None:
                raise forms.ValidationError('Repeat Interval/End missing', code='missing_repeat')
        return cleaned_data
