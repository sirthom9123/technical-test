import os
from flask import Flask
from flask_migrate import Migrate

app = Flask( __name__, static_folder='static')

app.secret_key = os.environ.get('SECRET_KEY')

# setup configs
env = os.environ.get('FLASK_ENV', 'development')

MAPBOX_KEY = os.environ.get('MAPBOX_API')
WEATHER_API = os.environ.get('WEATHER_API')

app.config['ENV'] = env
app.config.from_pyfile('config/%s.cfg' % env)

# CSRF protection
from flask_wtf.csrf import CSRFProtect
# CSRFProtect(app)

# Database
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#GZIP Compression
from flask_compress import Compress
Compress(app)