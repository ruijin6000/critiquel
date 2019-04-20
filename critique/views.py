from flask import render_template, request
from flask_pymongo import PyMongo
from . import app

states_list = {'Alabama': 'AL', 'Alaska': 'AK', 'American Samoa': 'AS', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District Of Columbia': 'DC', 'Federated States Of Micronesia': 'FM', 'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Marshall Islands': 'MH', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Northern Mariana Islands': 'MP', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Palau': 'PW', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}

mongo = PyMongo(app, uri="mongodb://ec2-54-241-147-8.us-west-1.compute.amazonaws.com:27022/yelpData")

@app.route('/business', methods=['POST', 'GET'])
def business():

    if request.method == 'POST':
        parameters = {}
        name = capitalize_each_word(request.form['name'])
        if len(name) > 0:
            parameters['name'] = name

        city = capitalize_each_word(request.form['city'])
        if len(city) > 0:
            parameters['city'] = city

        state_input = request.form['state']
        if len(state_input) > 0:
            state = state_input.upper() if len(state_input) == 2 else states_list[state_input.capitalize()]
            parameters['state'] = state

        ratings = request.form['ratings']
        if len(ratings) > 0:
            ratings = int(ratings)
            parameters['stars'] = {'$gte': ratings}

        projection = {'name': 1, 'city': 1, 'address': 1, 'categories': 1, 'stars': 1}

        result = mongo.db.business.find(parameters, projection).limit(20)
        return render_template('business.html', data=result)

    return render_template('business.html')

def capitalize_each_word(word):
    return ' '.join(i.capitalize() for i in word.split(" "))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.route('/businessByCity')
def businessByCity():
	result = mongo.db.business.find({'city':'Phoenix'}, {'name':1,'address':1,'categories':1})
	return render_template('businessByCity.html', data=result)

@app.route('/businessByName')
def businessByName():
	result = mongo.db.business.find({'name':'Arizona Biltmore Golf Club'}, {'name':1,'address':1,'city':1, 'state':1})
	return render_template('businessByCity.html', data=result)
