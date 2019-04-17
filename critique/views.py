from flask import render_template, request
from flask_pymongo import PyMongo
from . import app

# mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')
