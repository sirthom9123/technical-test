from datastories.app import app
from flask import request, url_for, flash, redirect, session, render_template
from sqlalchemy.sql import func
from datastories.models import db

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/home')
def home():
    return render_template('index.html')