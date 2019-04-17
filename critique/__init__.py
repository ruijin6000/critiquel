from flask import Flask

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://ec2-user@ec2-54-241-147-8.us-west-1.compute.amazonaws.com:27022/yelpData"

import critique.views
