import json
import pymongo
import logging
import traceback

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId as InvalidIdException
from flask import jsonify
from jsonschema import validate

db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/admin".format(db_username, db_password))
db = client["microservice1"]
coll = db["tasks"]


with open("task_schema.json", "rb") as f:
    task_schema = json.load(f)


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
    if not check_object(task, task_schema):
        return jsonify({"error": "Invalid task format."}), 400

    if "sub-tasks" in task and task["sub-tasks"]:
        for subtask in task["sub-tasks"]:
            if not check_object(subtask, task_schema):
                return jsonify({"error": "Invalid subtask format."}), 400
            # TODO: We should handle rollback here in case of an error while inserting
            subtask = {"_id": coll.insert_one(subtask).inserted_id}

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


##################################### HELPER FUNCTIONS #####################################


def check_task_fields(task):
    task_single_fields = ["name", "category", "department", "creator", 
    "description", "priority", "status", "deadline", "timestamp"]
    task_list_fields = {
        "participants": ["_id"],
        "sub-tasks": ["name", "description", "deadline", "status", "priority"],
        # "dependencies": ["task-id", "deadline", "status", "priority"],
        # "reverse-dependecies": ["task-id", "deadline", "status", "priority"],
        "dependencies": ["_id"],
        "reverse-dependecies": ["_id"],
        "commits": ["commit_url", "username", "changes", "timestamp"]
    }

    ret_obj, ret_val = check_custom_fields(task, task_single_fields)
    if not ret_val:
        return {"error": "Field {} is required but not present.".format(ret_obj)}, False

    for task_list_field in task_list_fields:
        if task_list_field in task:
            ret_obj[task_list_field] = []
            for task_list_field_entity in task[task_list_field]:
                ret_obj_child, ret_val = check_custom_fields(task_list_field_entity, task_list_fields[task_list_field])
                if not ret_val:
                    return {"error": "Field {} of one of the children of {} is required but not present.".format(ret_obj_child, task_list_field)}, False
                ret_obj[task_list_field].append(ret_obj_child)

    return {}, True


def check_custom_fields(obj, fields, ret_obj = {}):
    for field in fields:
        if field not in obj:
           return field, False
    for field in obj:
        if field in fields:
            ret_obj[field] = obj[field]
    return ret_obj, True

def check_object(obj, schema):
    try:
        validate(instance=obj, schema=schema)
        return True
    except:
        logging.error(traceback.format_exc())
        return False
