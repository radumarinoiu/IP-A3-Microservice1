import pymongo
import json

from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify

db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/tasks_db".format(db_username, db_password))
tasks_db = client["tasks_db"]
tasks = tasks_db["tasks"]

def getAll():
    getAll_cursor = tasks.find({})
    return list([elem["name"] for elem in getAll_cursor])

def getById(id):
    getById_cursor = tasks.find({"_id" : ObjectId(id)})
    return jsonify(list(elem["name"] for elem in getById_cursor))