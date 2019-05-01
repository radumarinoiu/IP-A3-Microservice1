import pymongo
import json

from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify
from flask import Response
from flask import make_response

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
    if not getByIdElem:
        return make_response(jsonify(""), 404)
    else:
        getByIdElem["_id"] = str(getByIdElem["_id"])
        return jsonify(getByIdElem)


def check_status(task):
    if task["status"] == "done":
        return True
    return False


def post_task(task):
    task_fields = ["name", "category", "department", "creator", 
    "description", "priority", "status", "deadline", "timestamp"]
    task_field_lists = {
        "participants": ["_id"],
        "sub-tasks": ["name", "description", "deadline", "status", "priority"],
        # "dependencies": ["task-id", "deadline", "status", "priority"],
        # "reverse-dependecies": ["task-id", "deadline", "status", "priority"],
        "dependencies": ["_id"],
        "reverse-dependecies": ["_id"],
        "commits": ["commit_url", "username", "changes", "timestamp"]
    }

    for field in task_fields:
        if field not in task:
            return {"error": "Field {} is required but not present.".format(field)}, 400

    for task_field in task_field_lists:
        if task_field in task:
            for task_field_field in task_field_lists[task_field]:
                if task_field_field not in task[task_field]:
                    return {"error": "Field {} from {} is required but not present.".format(
                        task_field_field, task_field)}, 400

    post_id = coll.insert_one(task).inserted_id
    return {"_id": str(post_id)}, 200


def put_task(task):
    if task["_id"] is "null":
        return "no id was sent"
    change = True
    if task["status"] == "done":
        for sub_task in task["sub-task"]:
            if check_status is False:
                change = False
                break
    if change == True:
        coll.update(
            { '_id': ObjectId(task['_id']) },
            { "$set": { 'status': 'done' } },
            upsert = False
        )
    
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
    # result = {'a' : 'b'}
    return make_response(jsonify(""), 200)

