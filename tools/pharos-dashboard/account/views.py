import os
import urllib

import oauth2 as oauth
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from jira import JIRA

from account.forms import AccountSettingsForm
from account.jira_util import SignatureMethod_RSA_SHA1
from account.models import UserProfile
from pharos_dashboard import settings

consumer = oauth.Consumer(settings.OAUTH_CONSUMER_KEY, settings.OAUTH_CONSUMER_SECRET)


@method_decorator(login_required, name='dispatch')
class AccountSettingsView(UpdateView):
    model = UserProfile
    form_class = AccountSettingsForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             'Settings saved')
        return '/'

    def get_object(self, queryset=None):
        return self.request.user.userprofile


class JiraLoginView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        client = oauth.Client(consumer)
        client.set_signature_method(SignatureMethod_RSA_SHA1())

        # Step 1. Get a request token from Jira.
        resp, content = client.request(settings.OAUTH_REQUEST_TOKEN_URL, "POST")
        if resp['status'] != '200':
            raise Exception("Invalid response %s: %s" % (resp['status'], content))

        # Step 2. Store the request token in a session for later use.
        self.request.session['request_token'] = dict(urllib.parse.parse_qsl(content.decode()))
        # Step 3. Redirect the user to the authentication URL.
        url = settings.OAUTH_AUTHORIZE_URL + '?oauth_token=' + \
              self.request.session['request_token']['oauth_token']
        return url


class JiraLogoutView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return '/'


class JiraAuthenticatedView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # Step 1. Use the request token in the session to build a new client.
        token = oauth.Token(self.request.session['request_token']['oauth_token'],
                            self.request.session['request_token']['oauth_token_secret'])
        client = oauth.Client(consumer, token)
        client.set_signature_method(SignatureMethod_RSA_SHA1())

        # Step 2. Request the authorized access token from Jira.
        resp, content = client.request(settings.OAUTH_ACCESS_TOKEN_URL, "POST")
        if resp['status'] != '200':
            return '/'

        access_token = dict(urllib.parse.parse_qsl(content.decode()))

        module_dir = os.path.dirname(__file__)  # get current directory
        with open(module_dir + '/rsa.pem', 'r') as f:
            key_cert = f.read()

        oauth_dict = {
            'access_token': access_token['oauth_token'],
            'access_token_secret': access_token['oauth_token_secret'],
            'consumer_key': settings.OAUTH_CONSUMER_KEY,
            'key_cert': key_cert
        }

        jira = JIRA(server=settings.JIRA_URL, oauth=oauth_dict)
        username = jira.current_user()
        url = '/'
        # Step 3. Lookup the user or create them if they don't exist.
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Save our permanent token and secret for later.
            user = User.objects.create_user(username=username,
                                            password=access_token['oauth_token_secret'])
            profile = UserProfile()
            profile.user = user
            profile.save()
            url = reverse('account:settings')
        user.userprofile.oauth_token = access_token['oauth_token']
        user.userprofile.oauth_secret = access_token['oauth_token_secret']
        user.userprofile.save()
        user.set_password(access_token['oauth_token_secret'])
        user.save()
        user = authenticate(username=username, password=access_token['oauth_token_secret'])
        login(self.request, user)
        # redirect user to settings page to complete profile
        return url
