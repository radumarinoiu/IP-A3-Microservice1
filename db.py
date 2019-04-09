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
    getAllList = list(tasks.find({}))
    for task in getAllList:
        task["_id"] = str(task["_id"])
    return jsonify(getAllList)

def getById(id):
    getByIdElem = tasks.find_one({"_id" : ObjectId(id)})
    getByIdElem["_id"] = str(getByIdElem["_id"])
    return jsonify(getByIdElem)
    
def post_task(task):
	post = {'nume': task["nume"], 'creare': task["creare"], 'expirare': task["expirare"]}
	posts = tasks
	post_id = posts.insert_one(post).inserted_id
	return post_id

def put_task(task):
    tasks.update(
        {'_id': task['_id']}, 
        { 
            '$set' : { "nume": task["nume"], "expirare": task["expirare"], "creare": task["creare"] }
        }
    )
	
