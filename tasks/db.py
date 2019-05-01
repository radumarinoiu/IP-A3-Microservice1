import pymongo
import json

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId as InvalidIdException
from flask import jsonify

db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/admin".format(db_username, db_password))
db = client["microservice1"]
coll = db["tasks"]


def getAll():
    tasks_list = list(coll.find({}))
    for task in tasks_list:
        task["_id"] = str(task["_id"])
    return jsonify(tasks_list), 200


def getById(task_id):
    try:
        task = coll.find_one({"_id" : ObjectId(task_id)})
    except InvalidIdException:
        return jsonify({"error": "Invalid id"}), 400
    if not task:
        return jsonify({}), 404
    else:
        task["_id"] = str(task["_id"])
        return jsonify(task), 200


def post_task(task):
    if not task:
        return jsonify({"error": "Empty request."}), 400
    
    # Check task's fields
    message, result = check_task_fields(task)
    if not result:
        return jsonify(message), 400

    post_id = coll.insert_one(task).inserted_id
    task["_id"] = str(post_id)
    return jsonify(task), 201


def put_task(task):
    if not task:
        return jsonify({"error": "Empty request."}), 400
    if "_id" not in task:
        return jsonify({"error": "Put request missing _id"}), 400
    
    # Check task's fields
    message, result = check_task_fields(task)
    if not result:
        return jsonify(message), 400

    task["_id"] = ObjectId(task["_id"])
    coll.update(
        {"_id": task["_id"]},
        {"$set": task},
        upsert=False)
    task["_id"] = str(task["_id"])
    return jsonify(task), 200


def deleteById(id):
    deletedId = coll.find_one({"_id" : ObjectId(id)})
    deletedId["_id"] = str(deletedId["_id"])
    coll.remove({"_id" : ObjectId(id)})
    return jsonify({}), 200


def check_task_fields(task):
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
            return jsonify({"error": "Field {} is required but not present.".format(field)}), False

    for field in list(field in task):
        if field not in task_fields and field not in task_field_lists:
            del task[field]


    for task_field_child in task_field_lists:
        if task_field_child in task:
            for task_field_child_field in task_field_lists[task_field_child]:
                if task_field_child_field not in task[task_field_child]:
                    return jsonify({"error": "Field {} from {} is required but not present.".format(
                        task_field_child_field, task_field_child)}), False

            for task_field_field in list(field in task[task_field_child]):
                if task_field_field not in task_field_lists[task_field_child]:
                    del task[task_field_field]

    return jsonify({}), True