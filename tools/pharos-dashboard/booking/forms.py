import django.forms as forms


class BookingForm(forms.Form):
    fields = ['start', 'end', 'purpose']

    start = forms.DateTimeField()
    end = forms.DateTimeField()
    purpose = forms.CharField(max_length=300)