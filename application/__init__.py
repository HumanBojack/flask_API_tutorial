from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from applicationinsights.flask.ext import AppInsights


app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
appinsights = AppInsights(app)


from application import routes
from application import models

models.init_db()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return models.User.query.get(user_id)

@app.after_request
def after_request(response):
  appinsights.flush()
  return response