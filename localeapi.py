from flask import Flask
from flask import jsonify
import json
from bson.json_util import dumps
from pymongo import MongoClient
import pprint

def mongoSession():
    mongodbUri = "mongodb://appadmin:hangout@ds032887.mlab.com:32887/hangout"
    return MongoClient(mongodbUri).hangout

app = Flask(__name__)

@app.route("/")
def home():
    return "You've reached Squiry"

@app.route("/GetRecommendations")
def getRecommendations():
    db = mongoSession()
    
    recommendations = []
    for place in db.places.find():
        recommendations.append(place)
    return dumps(recommendations)

@app.route("/GetPlacesbyCategory")
def getPlacesbyCategory():
    return "You've reached locale"


@app.route("/GetPlaceDetail")
def getPlaceDetail():
    return "You've reached locale"


@app.route("/GetPlacesbySubCategory")
def getPlacesbySubCategory():
    return "You've reached locale"

if __name__ == "__main__":
    app.run()