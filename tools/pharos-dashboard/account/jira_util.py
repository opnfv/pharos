import base64
import os

import oauth2 as oauth
from jira import JIRA
from tlslite.utils import keyfactory

from django.conf import settings


class SignatureMethod_RSA_SHA1(oauth.SignatureMethod):
    name = 'RSA-SHA1'

    def signing_base(self, request, consumer, token):
        if not hasattr(request, 'normalized_url') or request.normalized_url is None:
            raise ValueError("Base URL for request is not set.")

        sig = (
            oauth.escape(request.method),
            oauth.escape(request.normalized_url),
            oauth.escape(request.get_normalized_parameters()),
        )

        key = '%s&' % oauth.escape(consumer.secret)
        if token:
            key += oauth.escape(token.secret)
        raw = '&'.join(sig)
        return key, raw

    def sign(self, request, consumer, token):
        """Builds the base signature string."""
        key, raw = self.signing_base(request, consumer, token)

        module_dir = os.path.dirname(__file__)  # get current directory
        with open(module_dir + '/rsa.pem', 'r') as f:
            data = f.read()
        privateKeyString = data.strip()
        privatekey = keyfactory.parsePrivateKey(privateKeyString)
        raw = str.encode(raw)
        signature = privatekey.hashAndSign(raw)
        return base64.b64encode(signature)


def get_jira(user):
    module_dir = os.path.dirname(__file__)  # get current directory
    with open(module_dir + '/rsa.pem', 'r') as f:
        key_cert = f.read()

    oauth_dict = {
        'access_token': user.userprofile.oauth_token,
        'access_token_secret': user.userprofile.oauth_secret,
        'consumer_key': settings.OAUTH_CONSUMER_KEY,
        'key_cert': key_cert
    }

    return JIRA(server=settings.JIRA_URL, oauth=oauth_dict)