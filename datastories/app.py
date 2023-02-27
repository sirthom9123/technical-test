import os
from flask import Flask

app = Flask( __name__, static_folder='static')

app.secret_key = os.environ.get('SECRET_KEY')

# setup configs
env = os.environ.get('FLASK_ENV', 'development')

app.config['ENV'] = env
app.config.from_pyfile('config/%s.cfg' % env)

# CSRF protection
from flask_wtf.csrf import CSRFProtect
CSRFProtect(app)

# Database
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#GZIP Compression
from flask_compress import Compress
Compress(app)