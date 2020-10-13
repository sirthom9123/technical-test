from flask import request, url_for, flash, redirect, session,jsonify
from flask import render_template
from flask_security import current_user, login_required,url_for_security
from sqlalchemy.sql import func
from weather.models import *

@app.route('/')
def home():
    return render_template('layout.html')