##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import os
import urllib

import oauth2 as oauth
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, TemplateView, UpdateView

from jira import JIRA
from rest_framework.authtoken.models import Token

from account.forms import AccountSettingsForm
from account.jira_util import SignatureMethod_RSA_SHA1
from account.models import UserProfile


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

    def get_context_data(self, **kwargs):
        token, created = Token.objects.get_or_create(user=self.request.user)
        context = super(AccountSettingsView, self).get_context_data(**kwargs)
        context.update({'title': "Settings", 'token': token})
        return context


class JiraLoginView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        consumer = oauth.Consumer(settings.OAUTH_CONSUMER_KEY, settings.OAUTH_CONSUMER_SECRET)
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
              self.request.session['request_token']['oauth_token'] + \
              '&oauth_callback=' + settings.OAUTH_CALLBACK_URL
        return url


class JiraLogoutView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return '/'


class JiraAuthenticatedView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # Step 1. Use the request token in the session to build a new client.
        consumer = oauth.Consumer(settings.OAUTH_CONSUMER_KEY, settings.OAUTH_CONSUMER_SECRET)
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

@method_decorator(login_required, name='dispatch')
class UserListView(TemplateView):
    template_name = "account/user_list.html"

    def get_context_data(self, **kwargs):
        users = User.objects.all()
        context = super(UserListView, self).get_context_data(**kwargs)
        context.update({'title': "Dashboard Users", 'users': users})
        return context
