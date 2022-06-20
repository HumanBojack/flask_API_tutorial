from rauth import OAuth2Service
from application import app

class GoogleOAuth():

  def __init__(self):
    self.provider_name = "google"
    credentials = app.config["OAUTH_CREDENTIALS"]
    self.consumer_id = credentials['id']
    self.consumer_secret = credentials['secret']