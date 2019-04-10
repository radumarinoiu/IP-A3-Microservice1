import pymongo
import json

from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify

db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/assigner_db".format(db_username, db_password))
db = client["assigner_db"]
coll = db["assigner"]

def getAll():
    getAllList = list(coll.find({}))
    for task in getAllList:
        task["_id"] = str(task["_id"])
    return jsonify(getAllList)

def getById(id):
    getByIdElem = coll.find_one({"_id" : ObjectId(id)})
    getByIdElem["_id"] = str(getByIdElem["_id"])
    return jsonify(getByIdElem)

def post_assignement(assignement):
    post = {'id_user': assignement["id_user"], 'id_task': assignement["id_task"]}
    post_id = coll.insert_one(post).inserted_id
    return str(post_id)


def put_assignement(assignement):
    coll.update(
        { '_id': ObjectId(assignement['_id']) },
        { "$set": { 'id_user': assignement['id_user'], 'id_task': assignement['id_task'] } },
        upsert = False
    )
    return str(assignement['_id'])
