from app import routes
from app import models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '1234567893404040583930304'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db.init_app(app)
migrate = Migrate(app, db)

db.create_all()
db.session.commit()
