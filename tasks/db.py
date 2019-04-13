import pymongo
import json

from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify

db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/tasks_db".format(db_username, db_password))
db = client["tasks_db"]
coll = db["tasks"]

def getAll():
    getAllList = list(coll.find({}))
    for task in getAllList:
        task["_id"] = str(task["_id"])
    return jsonify(getAllList)

def getById(id):
    getByIdElem = coll.find_one({"_id" : ObjectId(id)})
    getByIdElem["_id"] = str(getByIdElem["_id"])
    return jsonify(getByIdElem)

def post_task(task):
    post = {'nume': task["nume"], 'creare': task["creare"], 'expirare': task["expirare"]}
    post_id = coll.insert_one(post).inserted_id
    return str(post_id)


def put_task(task):
    coll.update(
        { '_id': ObjectId(task['_id']) },
        { "$set": { 'nume': task['nume'], 'creare': task['creare'], 'expirare': task['expirare'] } },
        upsert = False
    )
    return str(task['_id'])

def deleteById(id):
    deletedId = coll.find_one({"_id" : ObjectId(id)})
    deletedId["_id"] = str(deletedId["_id"])
    coll.remove({"_id" : ObjectId(id)})
    return jsonify(deletedId)

