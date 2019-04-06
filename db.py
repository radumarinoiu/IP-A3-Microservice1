import pymongo
import json

from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/tasks_db".format(db_username, db_password))
tasks_db = client["tasks_db"]
tasks = tasks_db["tasks"]

def getAll():
    getAll_cursor = tasks.find({})
    return JSONEncoder().encode(list([elem for elem in getAll_cursor]))

def getById(id):
    getById_cursor = tasks.find({"_id" : ObjectId(id)})
    return jsonify(list(elem["name"] for elem in getById_cursor))