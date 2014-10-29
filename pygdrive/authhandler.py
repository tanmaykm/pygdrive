import base64
import datetime
import os

import tornado
import tornado.web
import tornado.gen
import tornado.httpclient
from tornado.auth import GoogleOAuth2Mixin
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI
from oauth2client.client import OAuth2Credentials, _extract_id_token

from handler_base import HandlerBase


class AuthHandler(HandlerBase, GoogleOAuth2Mixin):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        # self_redirect_uri should be similar to  'http://<host>/auth/'
        self_redirect_uri = self.request.full_url()
        idx = self_redirect_uri.index("auth/")
        self_redirect_uri = self_redirect_uri[0:(idx + len("auth/"))]

        code = self.get_argument('code', False)

        if code is not False:
            user = yield self.get_authenticated_user(redirect_uri=self_redirect_uri, code=code)
            self.logger.debug("got user: " + repr(user))
            creds = self.make_credentials(user)
            tokfile = self.settings['token_file']
            tokdir = os.path.dirname(tokfile)
            if not os.path.exists(tokdir):
                os.makedirs(tokdir)
            os.chmod(tokdir, 0700)
            with open(tokfile, 'w') as gtok_file:
                gtok_file.write(base64.b64encode(creds.to_json()))
            self.redirect('/')
            return
        else:
            scope = ['https://www.googleapis.com/auth/drive', 'email']
            extra_params = {
                'approval_prompt':          'auto',  # auto / force
                'access_type':              'offline',
                'include_granted_scopes':   'true'
            }

            yield self.authorize_redirect(redirect_uri=self_redirect_uri,
                                          client_id=self.settings['google_oauth']['key'],
                                          scope=scope,
                                          response_type='code',
                                          extra_params=extra_params)

    def make_credentials(self, user):
        token_expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(user['expires_in']))
        id_token = _extract_id_token(user['id_token'])
        credential = OAuth2Credentials(
            access_token=user['access_token'],
            client_id=self.settings['google_oauth']['key'],
            client_secret=self.settings['google_oauth']['secret'],
            refresh_token=user['refresh_token'],
            token_expiry=token_expiry,
            token_uri=GOOGLE_TOKEN_URI,
            user_agent=None,
            revoke_uri=GOOGLE_REVOKE_URI,
            id_token=id_token,
            token_response=user)
        return credential
