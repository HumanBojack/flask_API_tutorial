from rauth import OAuth2Service
from application import app
from flask import redirect, request
import json
import os

class GoogleOAuth():

  def __init__(self):
    self.provider_name = "google"
    credentials = app.config["OAUTH_CREDENTIALS"]
    self.client_id = credentials['id']
    self.client_secret = credentials['secret']

    self.service = OAuth2Service(
      name = "google",
      client_id = self.client_id,
      client_secret = self.client_secret,
      authorize_url = "https://accounts.google.com/o/oauth2/auth",
      access_token_url = "https://oauth2.googleapis.com/token",
      base_url = "https://www.googleapis.com/oauth2/v1/certs"
    )

  def authorize(self):
    return redirect(self.service.get_authorize_url(
      scope='email',
      response_type='code',
      redirect_uri= os.environ.get('URL') + "/callback"
    ))

  def callback(self):
    def decode_json(payload):
      print(payload)
      return json.loads(payload.decode('utf-8'))

    if 'code' not in request.args:
      return None, None, None

    print(self.client_id, self.client_secret, request.args['code'])

    # request_token, request_token_secret = self.service.get_request_token()

    oauth_session = self.service.get_auth_session(
      data={'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': os.environ.get('URL') + "/callback"
            },
      decoder=decode_json
    )
    print(oauth_session)

    user = oauth_session.get('userinfo').json()
    print(user)
    id = user.get("id")
    email = user.get("email")
    name = user.get("email").split("@")[0]

    return id, email, name