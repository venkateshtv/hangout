from flask import Flask
from flask import jsonify
from flask import request
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
import pprint

def mongoSession():
    mongodbUri = "mongodb://admin:squiry@ds032887.mlab.com:32887/hangout"
    return MongoClient(mongodbUri).hangout

app = Flask(__name__)

@app.route("/")
def home():
    return "You've reached Squiry"

@app.route("/GetRecommendations")
def getRecommendations():
    db= mongoSession()    
    pipeline = [{"$group":{"_id":"$category", "places": {"$addToSet":"$$ROOT"}}}]
    placesByCategory = db.places.aggregate(pipeline)
    recommendations = []
    for category in placesByCategory:        
        for index,place in enumerate(category['places']):
            if index <= 1:
                recommendations.append(place)
    return dumps(recommendations)

@app.route("/GetPlacesCategories")
def getPlacesCategories():
    db = mongoSession()   
    pipeline = [{"$group":{"_id":"$category", "count": {"$sum":1}}}]
    result = db.places.aggregate(pipeline)
    return dumps(result)

@app.route("/GetPlacesbyCategory/<string:category>")
def getPlacesbyCategory(category):
    db = mongoSession()    
    result = db.places.find({"category":category})
    return dumps(result)

@app.route("/GetPlaceDetail/<string:place_id>")
def getPlaceDetail(place_id):
    db= mongoSession()
    result = db.places.find({"_id":ObjectId(place_id)})
    return dumps(result)

@app.route("/SearchPlaces",methods=['POST'])
def searchPlaceByName():        
    searchParams = request.get_json()
    if not searchParams['searchText']:
        raise "No params found"
    searchQuery = []
    searchQuery.append({'place':{'$regex':searchParams['searchText'],'$options':'i'}})
    searchQuery.append({'category': {'$regex':searchParams['searchText'],'$options':'i'}})
    searchQuery.append({'subcategory': {'$regex':searchParams['searchText'],'$options':'i'}})
    searchQuery.append({'city': {'$regex':searchParams['searchText'],'$options':'i'}})
    searchQuery.append({'area': {'$regex':searchParams['searchText'],'$options':'i'}})
    db= mongoSession()
    result = db.places.find({'$or':searchQuery})
    return dumps(result)

if __name__ == "__main__":
    app.run()