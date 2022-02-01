
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)


from api_modele_demo import views
from api_modele_demo import models

models.init_db()