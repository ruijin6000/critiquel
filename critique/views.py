from flask import render_template, request
from flask_pymongo import PyMongo
from . import app

mongo = PyMongo(app, uri="mongodb://ec2-54-241-147-8.us-west-1.compute.amazonaws.com:27022/yelpData")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.route('/business')
def business():
    print()
    result = mongo.db.business.find({'state':'CA'}, {'name':1,'address':1,'categories':1})
    # result = mongo.db.business.find({'city':'Phoenix'}, {'name':1,'address':1,'categories':1})
    return render_template('business.html', data=result)


@app.route('/businessByCity')
def businessByCity():
	print()
	result = mongo.db.business.find({'city':'Phoenix'}, {'name':1,'address':1,'categories':1})
	return render_template('businessByCity.html', data=result)

@app.route('/businessByName')
def businessByName():
	print()
	result = mongo.db.business.find({'name':'Arizona Biltmore Golf Club'}, {'name':1,'address':1,'city':1, 'state':1})
	return render_template('businessByCity.html', data=result)