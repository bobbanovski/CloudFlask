from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

#migrations
migrate = Migrate(app, db)

from blog import views # need to import for every folder
from author import views