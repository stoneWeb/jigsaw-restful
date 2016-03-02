from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_mail import Mail
from flask.ext.cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object('config')

mail = Mail()
db = MongoEngine(app)
mail.init_app(app)

from app import api_resource, models, auth
