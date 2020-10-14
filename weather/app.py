import os
from flask import Flask
from flask_login import LoginManager

app = Flask(
    __name__,
    static_folder='static')

app.secret_key = app.config['SECRET_KEY']

# setup configs
env = os.environ.get('FLASK_ENV', 'develop')
app.config['ENV'] = env
app.config.from_pyfile('config/%s.cfg' % env)

# CSRF protection
from flask_wtf.csrf import CSRFProtect
csrf_protect = CSRFProtect(app)

# Database
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECURITY_REGISTERABLE'] = True

# Mail
from flask_mail import Mail
mail = Mail(app)


from flask_sslify import SSLify
ssl = SSLify(app)