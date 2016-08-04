import django.forms as forms


class AccountSettingsForm(forms.Form):
    fields = ['first_name', 'last_name', 'email', 'company', 'ssh_public_key']

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    company = forms.CharField(max_length=30)
    ssh_public_key = forms.CharField(max_length=2048, widget=forms.Textarea)

