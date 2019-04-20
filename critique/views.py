from flask import render_template, request
from flask_pymongo import PyMongo
from . import app

states_list = {'Alabama': 'AL', 'Alaska': 'AK', 'American Samoa': 'AS', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District Of Columbia': 'DC', 'Federated States Of Micronesia': 'FM', 'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Marshall Islands': 'MH', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Northern Mariana Islands': 'MP', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Palau': 'PW', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}

mongo = PyMongo(app, uri="mongodb://ec2-54-241-147-8.us-west-1.compute.amazonaws.com:27022/yelpData")

def capitalize_each_word(word):
    return ' '.join(i.capitalize() for i in word.split(" "))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.route('/business', methods=['POST', 'GET'])
def business():
    # Query field will never be empty since input is mandatory
    # If user inputted data in the form, we would have a post request.
    if request.method == 'POST':
        search_dictionary = {}
        # Get the input using the form fields and capitalize each word
        name = capitalize_each_word(request.form['name'])
        if len(name) > 0:
            search_dictionary['name'] = name

        city = capitalize_each_word(request.form['city'])
        if len(city) > 0:
            search_dictionary['city'] = city

        state_input = request.form['state']
        if len(state_input) > 0:
            state = state_input.upper() if len(state_input) == 2 else states_list[state_input.capitalize()]
            search_dictionary['state'] = state

        ratings = int(request.form['ratings'])
        print(ratings)
        search_dictionary['stars'] = ratings
        # Search parameters

        # Projection parameter
        projection = {'name': 1, 'city': 1, 'address': 1, 'categories': 1, 'stars': 1}

        # Get the query result and pass it to render the template
        print(f'db.business.find({search_dictionary},{projection})')
        result = mongo.db.business.find(search_dictionary, projection).limit(20)
        return render_template('business.html', data=result)
    # Else we have a get request, so don't pass data (will be None by default)
    return render_template('business.html')
