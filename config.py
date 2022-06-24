import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SECRET_KEY = os.environ.get('SECRET_KEY')

OAUTH_CREDENTIALS = {
        'id': os.environ.get('OAUTH_GOOGLE_ID'),
        'secret': os.environ.get('OAUTH_GOOGLE_SECRET')
        }

APPINSIGHTS_INSTRUMENTATIONKEY = os.environ.get('APPINSIGHTS_INSTRUMENTATIONKEY')
