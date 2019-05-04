from flask import render_template, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from . import app

states_list = {'Alabama': 'AL', 'Alaska': 'AK', 'American Samoa': 'AS', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District Of Columbia': 'DC', 'Federated States Of Micronesia': 'FM', 'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Marshall Islands': 'MH', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Northern Mariana Islands': 'MP', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Palau': 'PW', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}

mongo = PyMongo(app, uri="mongodb://ec2-54-241-147-8.us-west-1.compute.amazonaws.com:27022/yelpData")

@app.route('/business_search', methods=['POST', 'GET'])
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
            parameters['stars'] = ratings

        projection = {'name': 1, 'city': 1, 'address': 1, 'categories': 1, 'stars': 1}

        result = mongo.db.business.find(parameters, projection).limit(20)
        return render_template('business.html', data=result)

    return render_template('business.html')

@app.route('/tips', methods=['POST', 'GET'])
def tips():
    if request.method == 'POST':
        name = capitalize_each_word(request.form['name'])
        bus_id = mongo.db.business.find_one({'name':name},{"business_id":1})['business_id']
        tips = mongo.db.tips.find({"business_id": bus_id}, {"text":1, "date":1})
        return render_template('tips.html', data = tips)
    return render_template('tips.html')

@app.route('/check-in', methods=['POST', 'GET'])
def business_check_in():
    if request.method == 'POST':
        name = capitalize_each_word(request.form['name'])
        bus_id = mongo.db.business.find_one({'name':name},{"business_id":1})['business_id']
        dates = mongo.db.checkin.find_one({"business_id": bus_id}, {"date":1})['date']
        return render_template('checkins.html', data = {"dates": dates, "name": name})
    return render_template('checkins.html')

@app.route('/rate', methods=['POST', 'GET'])
def rate():
    if request.method == 'POST':
        name = capitalize_each_word(request.form['name'])
        user_rating = float(request.form['rating'])
        business = mongo.db.business.find_one({'name':name})
        reviews = business['review_count']
        old_rating = business['stars']
        new_rating = round((reviews*old_rating + user_rating)/(reviews+1), 2)
        result = mongo.db.business.update_one({"_id": ObjectId(business["_id"])}, {'$set': {'stars': new_rating, 'review_count': reviews+1}})
        increased = (new_rating - old_rating) > 0
        output = "" if result.modified_count == 0 else f"Your review has been recorded. Rating was {'increased' if increased else 'decreased'} from {old_rating} to {new_rating} for {name}."

        return render_template('rate.html', data = output)
    return render_template('rate.html')

@app.route('/business-hours', methods=['POST', 'GET'])
def business_hours():
    if request.method == 'POST':
        name = capitalize_each_word(request.form['name'])
        city = capitalize_each_word(request.form['city'])
        datum = mongo.db.business.find_one({'name':name, 'city': city})
        address = f"{datum['address']}, {datum['city']}, {datum['state']}."
        return render_template('business_hours.html', data = {'name': name, 'address': address, 'hours': datum['hours']})
    return render_template('business_hours.html')

@app.route('/restaurants-price-range', methods=['POST', 'GET'])
def restaurants_price_range():
    if request.method == 'POST':
        city = capitalize_each_word(request.form['city'])
        pr = request.form['range']
        data = mongo.db.business.find({'city': city, 'attributes.RestaurantsPriceRange2': pr, 'categories': {'$regex': 'Restaurants'}}).limit(20)

        return render_template('restaurants_price_range.html', data = data)
    return render_template('restaurants_price_range.html')

@app.route('/kids-friendly', methods=['POST', 'GET'])
def kids_friendly():
    if request.method == 'POST':
        name = capitalize_each_word(request.form['name']).strip()
        city = capitalize_each_word(request.form['city'])
        parameters = {'city': city, "attributes.GoodForKids": "True"}
        if len(name) != 0:
            parameters['name'] = name
            data = mongo.db.business.find_one(parameters, {'name': 1, 'address':1})
            cursor = False
        else:
            data = mongo.db.business.find(parameters, {'name': 1, 'address':1})
            cursor = True
        return render_template('kids_friendly.html', data=[data, cursor])
    return render_template('kids_friendly.html')

@app.route('/review-star', methods=['POST', 'GET'])
def business_more_than_x_reviews_y_stars():
    if request.method == 'POST':
        reviews = float(request.form['review'])
        ratings = float(request.form['rating'])
        city = capitalize_each_word(request.form['city'])
        parameters = {'review_count': {'$gte': reviews}, 'stars': {'$gte': ratings}}
        if len(city) != 0:
            parameters['city'] = city
        data = mongo.db.business.find(parameters, {'name': 1, 'address':1}).limit(20)
        return render_template('review_rating.html', data=data)
    return render_template('review_rating.html')

@app.route('/best-nights', methods=['POST', 'GET'])
def best_nights():
    if request.method == 'POST':
        name = capitalize_each_word(request.form['name'])
        city = capitalize_each_word(request.form['city'])
        parameters = {'name': name, 'city': city}
        data = mongo.db.business.find_one(parameters, {'attributes':1})['attributes']['BestNights'].replace('{','').replace('}','').split(',')
        days = []
        for i in data:
            j = i.split(":")
            if j[1].strip() == "True":
                days.append(j[0].strip().replace("'",'').capitalize())

        return render_template('best_nights.html', data={'days': ', '.join(days), 'name': name, 'city':city})
    return render_template('best_nights.html')

@app.route('/open-close', methods=['POST', 'GET'])
def business_open_or_close():
    if request.method == 'POST':
        name = capitalize_each_word(request.form['name'])
        parameters = {}
        if len(name) != 0:
            parameters['name'] = name
        city = capitalize_each_word(request.form['city'])
        if len(city) != 0:
            parameters['city'] = city
        projection = {'name': 1, 'city': 1, 'is_open':1}
        result = mongo.db.business.find(parameters, projection).limit(5)
        return render_template('business_open.html', data=result)
    return render_template('business_open.html')

@app.route('/no-checkin', methods=['GET'])
def business_no_checkin():
    data = mongo.db.checkin.find({'date': {'$size': 0}}, {'business_id':1})
    ids = [i['business_id'] for i in data]
    result = mongo.db.business.find({'business_id': {'$in': ids}})
    return render_template('business_no_checkin.html', data=result)

@app.route('/insert', methods=['POST', 'GET'])
def insert():
    if request.method == 'POST':
        name = capitalize_each_word(request.form['name'])
        address = capitalize_each_word(request.form['address'])
        city = capitalize_each_word(request.form['city'])
        state_input = request.form['state']
        if len(state_input) > 0:
            state = state_input.upper() if len(state_input) == 2 else states_list[state_input.capitalize()]
        category = capitalize_each_word(request.form['category'])
        attributes = {i: True for i in capitalize_each_word(request.form['services']).split(",")}
        ratings = capitalize_each_word(request.form['ratings'])
        result = mongo.db.business.insert_one({'name': name, 'address': address, 'city': city,
                                                'state': state, 'categories': category, 'attributes':attributes, 'stars': ratings})
        return render_template('insert.html', success=True)
    return render_template('insert.html')

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    status = 0                     # 0 means we need user input
    if request.method == 'POST':
        name = capitalize_each_word(request.form['name'])
        address = capitalize_each_word(request.form['address'])
        city = capitalize_each_word(request.form['city'])
        state_input = request.form['state']
        if len(state_input) > 0:
            state = state_input.upper() if len(state_input) == 2 else states_list[state_input.capitalize()]

        result = mongo.db.business.delete_one({'name': name, 'address': address, 'city':city, 'state':state})
        status = 1 if result.deleted_count == 1 else -1
        return render_template('delete.html', success=status)
    return render_template('delete.html', success=status)

@app.route('/update', methods=['POST', 'GET'])
def update():
    status = 0                     # 0 means we need user input
    if request.method == 'POST':
        name = capitalize_each_word(request.form['name'])
        address = capitalize_each_word(request.form['address'])
        city = capitalize_each_word(request.form['city'])
        state_input = request.form['state']
        if len(state_input) > 0:
            state = state_input.upper() if len(state_input) == 2 else states_list[state_input.capitalize()]
        new_rating = int(request.form['rating'])

        result = mongo.db.business.update_one({'name': name, 'address': address, 'city':city, 'state':state}, {'$set': {'stars':new_rating}})
        status = 1 if result.modified_count == 1 else -1
        return render_template('update.html', success=status)
    return render_template('update.html', success=status)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

def capitalize_each_word(word):
    return ' '.join(i.capitalize() for i in word.split(" "))
